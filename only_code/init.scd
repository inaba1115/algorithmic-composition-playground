SuperDirt.start;

(
SynthDef(\test, {
    |out, sustain=1, freq=440, speed=1, begin=0, end=1, pan, accelerate, offset|
    var env = Line.ar(1, 0, sustain);
    var osc = SinOsc.ar(freq);
    var output = osc * env;
    OffsetOut.ar(out, Pan2.ar(in: output, pos: pan));
}).add;
)
