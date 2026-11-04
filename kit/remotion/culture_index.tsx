import React from "react";
import {
  AbsoluteFill, Audio, Loop, OffthreadVideo, Composition, Sequence, registerRoot, staticFile,
  interpolate, spring, useCurrentFrame, useVideoConfig, delayRender, continueRender, Easing,
} from "remotion";
import props from "../public/culture/props.json";

const FPS = 30;
const DUR = 32.424;
const YEL = "#FFC400", RED = "#BE1428";
const fontHandle = delayRender();
new FontFace("Anton", `url(${staticFile("culture/Anton.ttf")})`).load().then((f) => {
  (document as any).fonts.add(f);
  continueRender(fontHandle);
}).catch(() => continueRender(fontHandle));

type Scene = { s: number; e: number; clip: string };
const SCENES: Scene[] = [
  { s: 0, e: 7.3, clip: "espace_soleil" },
  { s: 7.3, e: 15.2, clip: "espace_soleil2" },
  { s: 15.2, e: 22.1, clip: "espace_venus" },
  { s: 22.1, e: 26.0, clip: "espace_lune" },
  { s: 26.0, e: 33.0, clip: "espace_etoiles" },
];
const OV = 8; // frames de fondu enchaîné

const stroke: React.CSSProperties = {
  fontFamily: "Anton", color: "#fff", WebkitTextStroke: "10px #000", paintOrder: "stroke fill",
  textShadow: "0 8px 40px rgba(0,0,0,.6)", textAlign: "center", lineHeight: 1,
};

const SceneBg: React.FC<{ sc: Scene; i: number }> = ({ sc, i }) => {
  const f = useCurrentFrame();
  const n = Math.round((sc.e - sc.s) * FPS) + OV;
  const z = interpolate(f, [0, n], [1.05, 1.2], { easing: Easing.out(Easing.quad) });
  const op = i === 0 ? 1 : interpolate(f, [0, OV], [0, 1], { extrapolateRight: "clamp" });
  const punch = 1 + 0.07 * Math.exp(-f / 4);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <AbsoluteFill style={{ transform: `scale(${z * punch}) translateX(${interpolate(f, [0, n], [0, i % 2 ? 30 : -30])}px)` }}>
        <Loop durationInFrames={210}>
          <OffthreadVideo src={staticFile(`culture/${sc.clip}.mp4`)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
        </Loop>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,.05) 35%, rgba(0,0,0,.05) 60%, rgba(0,0,0,.7) 100%)" }} />
    </AbsoluteFill>
  );
};

const useT = () => useCurrentFrame() / FPS;
const pop = (f: number, t0: number) => {
  return spring({ frame: f - t0 * FPS, fps: FPS, config: { damping: 11, stiffness: 160, mass: 0.7 } });
};
const ease = (t: number, a: number, b: number, from = 0, to = 1) =>
  interpolate(t, [a, b], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
const show = (t: number, a: number, b: number) => (t >= a && t < b ? 1 : 0);
const fmt = (v: number, d = 0) => v.toFixed(d).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, " ");

const Chip: React.FC<{ text: string; t0: number; t1: number; y: number }> = ({ text, t0, t1, y }) => {
  const f = useCurrentFrame();
  if (f / FPS < t0 || f / FPS >= t1) return null;
  const p = pop(f, t0) * interpolate(f / FPS, [t1 - 0.2, t1], [1, 0], { extrapolateLeft: "clamp" });
  return (
    <div style={{ position: "absolute", top: y, left: 0, right: 0, display: "flex", justifyContent: "center", transform: `scale(${p})`, opacity: Math.min(1, p) }}>
      <div style={{ background: RED, color: YEL, fontFamily: "Anton", fontSize: 62, padding: "10px 36px", borderRadius: 12, boxShadow: "0 10px 30px rgba(0,0,0,.5)" }}>{text}</div>
    </div>
  );
};

const BigNum: React.FC<{ t0: number; t1: number; to: number; dec?: number; suffix?: string; prefix?: string; size?: number; y?: number; dur?: number }> = (a) => {
  const f = useCurrentFrame();
  const t = useT();
  if (t < a.t0 || t >= a.t1) return null;
  const p = pop(f, a.t0);
  const v = ease(t, a.t0, a.t0 + (a.dur ?? 1.0), 0, a.to);
  const out = interpolate(t, [a.t1 - 0.15, a.t1], [1, 0], { extrapolateLeft: "clamp" });
  return (
    <div style={{ position: "absolute", top: a.y ?? 560, left: 0, right: 0, ...stroke, fontSize: a.size ?? 230, transform: `scale(${0.6 + 0.4 * p})`, opacity: out * Math.min(1, p * 2) }}>
      {a.prefix}{fmt(v, a.dec ?? 0)}{a.suffix}
    </div>
  );
};

const Clock: React.FC<{ t0: number; t1: number }> = ({ t0, t1 }) => {
  const f = useCurrentFrame();
  const t = useT();
  if (t < t0 || t >= t1) return null;
  const sec = Math.round(ease(t, t0, t0 + 1.2, 0, 500));
  const p = pop(f, t0);
  const out = interpolate(t, [t1 - 0.15, t1], [1, 0], { extrapolateLeft: "clamp" });
  return (
    <div style={{ position: "absolute", top: 520, left: 0, right: 0, ...stroke, fontSize: 260, transform: `scale(${0.6 + 0.4 * p})`, opacity: out }}>
      {String(Math.floor(sec / 60)).padStart(2, "0")}:{String(sec % 60).padStart(2, "0")}
    </div>
  );
};

const Ring: React.FC<{ t0: number; t1: number; pct: number }> = ({ t0, t1, pct }) => {
  const t = useT();
  if (t < t0 || t >= t1) return null;
  const R = 300, C = 2 * Math.PI * R;
  const k = ease(t, t0, t0 + 1.4);
  const out = interpolate(t, [t1 - 0.2, t1], [1, 0], { extrapolateLeft: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <svg width="1080" height="1920" style={{ position: "absolute", inset: 0 }}>
        <circle cx={540} cy={700} r={R} stroke="rgba(255,255,255,.18)" strokeWidth={46} fill="none" />
        <circle cx={540} cy={700} r={R} stroke={YEL} strokeWidth={46} fill="none" strokeLinecap="round"
          strokeDasharray={C} strokeDashoffset={C * (1 - (pct / 100) * k)} transform="rotate(-90 540 700)" style={{ filter: "drop-shadow(0 0 24px rgba(255,196,0,.8))" }} />
      </svg>
      <div style={{ position: "absolute", top: 610, left: 0, right: 0, ...stroke, fontSize: 170 }}>{fmt(pct * k, 2)} %</div>
    </AbsoluteFill>
  );
};

const Bars: React.FC<{ t0: number; t1: number }> = ({ t0, t1 }) => {
  const t = useT();
  if (t < t0 || t >= t1) return null;
  const out = interpolate(t, [t1 - 0.2, t1], [1, 0], { extrapolateLeft: "clamp" });
  const bar = (label: string, val: number, max: number, ta: number, y: number, col: string) => {
    const k = ease(t, ta, ta + 0.9);
    return (
      <div style={{ position: "absolute", top: y, left: 90, width: 900, height: 150, opacity: k > 0 ? 1 : 0 }}>
        <div style={{ width: 900 * (val / max) * k, height: 150, background: col, borderRadius: 18, boxShadow: "0 14px 40px rgba(0,0,0,.5)", display: "flex", alignItems: "center", paddingLeft: 30, overflow: "hidden", whiteSpace: "nowrap" }}>
          <span style={{ fontFamily: "Anton", fontSize: 76, color: "#fff" }}>{label} {Math.round(val * k)} J</span>
        </div>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{ opacity: out }}>
      {bar("1 JOUR =", 243, 243, t0, 520, RED)}
      {bar("1 AN =", 225, 243, 20.91, 720, "#1E6FD9")}
    </AbsoluteFill>
  );
};

const Moon: React.FC<{ t0: number; t1: number }> = ({ t0, t1 }) => {
  const f = useCurrentFrame();
  const t = useT();
  if (t < t0 || t >= t1) return null;
  const k = ease(t, t0 + 0.2, t0 + 1.6);
  const out = interpolate(t, [t1 - 0.2, t1], [1, 0], { extrapolateLeft: "clamp" });
  const p = pop(f, t0);
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <svg width="1080" height="1920" style={{ position: "absolute", inset: 0 }}>
        <circle cx={250} cy={800} r={150} fill="#1E6FD9" style={{ filter: "drop-shadow(0 0 40px rgba(60,140,255,.8))" }} />
        <circle cx={700 + 120 * k} cy={800} r={52} fill="#dcdcdc" style={{ filter: "drop-shadow(0 0 20px rgba(255,255,255,.6))" }} />
        <line x1={420} y1={800} x2={640 + 120 * k} y2={800} stroke={YEL} strokeWidth={8} strokeDasharray="22 16" />
      </svg>
      <div style={{ position: "absolute", top: 450, left: 0, right: 0, ...stroke, fontSize: 200, transform: `scale(${0.6 + 0.4 * p})` }}>+{fmt(3.8 * ease(t, t0, t0 + 0.8), 1)} CM</div>
    </AbsoluteFill>
  );
};

const CTA: React.FC<{ t0: number }> = ({ t0 }) => {
  const f = useCurrentFrame();
  const t = useT();
  if (t < t0) return null;
  const p1 = pop(f, t0), p2 = pop(f, 28.97);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 560, left: 0, right: 0, ...stroke, fontSize: 135, whiteSpace: "nowrap", transform: `scale(${0.6 + 0.4 * p1})` }}>TU CONNAISSAIS ?</div>
      {t >= 28.97 && (
        <div style={{ position: "absolute", top: 830, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 30, transform: `scale(${p2})` }}>
          <div style={{ background: RED, color: "#fff", fontFamily: "Anton", fontSize: 80, padding: "14px 40px", borderRadius: 18 }}>♥ LIKE</div>
          <div style={{ background: YEL, color: "#000", fontFamily: "Anton", fontSize: 80, padding: "14px 40px", borderRadius: 18 }}>ABONNE-TOI +</div>
        </div>
      )}
    </AbsoluteFill>
  );
};

const Captions: React.FC = () => {
  const t = useT();
  const blocks: any[][] = (props as any).blocks;
  for (let bi = 0; bi < blocks.length; bi++) {
    const b = blocks[bi];
    const nxt = bi + 1 < blocks.length ? blocks[bi + 1][0].s : 1e9;
    const t0 = b[0].s, t1 = Math.min(b[b.length - 1].e + 0.3, nxt);
    if (t >= t0 - 0.02 && t < t1) {
      const sc = interpolate(t, [t0, t0 + 0.12], [0.85, 1], { extrapolateRight: "clamp" });
      return (
        <div style={{ position: "absolute", top: 1290, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 24, transform: `scale(${sc})` }}>
          {b.map((w, i) => {
            const active = t >= w.s && (i === b.length - 1 || t < b[i + 1].s);
            return <span key={i} style={{ ...stroke, WebkitTextStroke: "9px #000", fontSize: 92, color: active ? YEL : "#fff", transform: active ? "scale(1.12)" : "none" }}>{w.w}</span>;
          })}
        </div>
      );
    }
  }
  return null;
};

const Cut: React.FC<{ at: number }> = ({ at }) => {
  const t = useT();
  const o = interpolate(t, [at, at + 0.15], [0.55, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return o > 0 && t >= at ? <AbsoluteFill style={{ background: "#fff", opacity: o }} /> : null;
};

const Video: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {SCENES.map((sc, i) => {
        const from = Math.max(0, Math.round(sc.s * FPS) - (i ? OV : 0));
        const dur = Math.round((sc.e - sc.s) * FPS) + (i ? OV : 0) + 1;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <SceneBg sc={sc} i={i} />
          </Sequence>
        );
      })}
      <Clock t0={0.08} t1={5.3} />
      <Chip text="LA LUMIÈRE DU SOLEIL → TOI" t0={0.6} t1={5.3} y={820} />
      <BigNum t0={5.44} t1={7.3} to={300000} suffix=" KM/S" size={190} y={560} dur={0.9} />
      <Chip text="LA VITESSE DE LA LUMIÈRE" t0={5.9} t1={7.3} y={800} />
      <Ring t0={8.92} t1={15.2} pct={99.86} />
      <Chip text="DE LA MASSE DU SYSTÈME SOLAIRE" t0={9.6} t1={15.2} y={1060} />
      <Bars t0={17.03} t1={22.1} />
      <Chip text="SUR VÉNUS" t0={16.5} t1={22.1} y={420} />
      <Moon t0={24.4} t1={26.0} />
      <Chip text="LA LUNE S'ÉLOIGNE CHAQUE ANNÉE" t0={24.9} t1={26.0} y={1060} />
      <CTA t0={26.17} />
      <Captions />
      {SCENES.slice(1).map((sc, i) => <Cut key={i} at={sc.s} />)}
      <Audio src={staticFile("culture/mix.wav")} />
    </AbsoluteFill>
  );
};

const Root: React.FC = () => (
  <Composition id="Culture" component={Video} durationInFrames={Math.round(DUR * FPS)} fps={FPS} width={1080} height={1920} />
);
registerRoot(Root);
