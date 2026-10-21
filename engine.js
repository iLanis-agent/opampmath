// Op-amp Math engine: non-inverting gain, inverting gain, and a two-input summing stage. Exact integers (ohms, hundredths of a V), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pi(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,7}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _R = "each resistance must be a whole number from 1 to 1000000 Ω";
var _V = "each voltage must be from 0.01 to 10 V with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  if (v < 0) return "-" + _dec(-v, places);
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _v(v) { return _dec(v, 2) + " V"; }
function _ohm(r) { return r + " Ω"; }
function _r(t) { return _pi(t, _R, 1, 1000000); }
function _vin(t) { return _p(t, _V, 2, 2, 1, 1000); }

function noninvTruth(rf, rg, vin) {
  var f = _r(rf), g = _r(rg), v = _vin(vin);
  var gain = _hu((f + g) * 100, g), out = _hu(v * (f + g), g);
  return "A " + _ohm(f) + " feedback over a " + _ohm(g) + " to ground gives a gain of " + _dec(gain, 2) + ". " + _v(v) + " in comes out at " + _v(out) + ".";
}
function invTruth(rf, rin, vin) {
  var f = _r(rf), n = _r(rin), v = _vin(vin);
  var gain = _hu(f * 100, n), out = _hu(v * f, n);
  return "With " + _ohm(f) + " feedback and " + _ohm(n) + " in, the gain is " + (gain ? "-" : "") + _dec(gain, 2) + ". " + _v(v) + " in comes out at " + (out ? "-" : "") + _v(out) + ".";
}
function sumTruth(rf, r1, v1, r2, v2) {
  var f = _r(rf), a = _r(r1), b = _r(r2), x = _vin(v1), y = _vin(v2);
  var out = _hu(f * (x * b + y * a), a * b);
  return "With " + _ohm(f) + " feedback, " + _v(x) + " through " + _ohm(a) + " and " + _v(y) + " through " + _ohm(b) + " sum to " + (out ? "-" : "") + _v(out) + ".";
}
