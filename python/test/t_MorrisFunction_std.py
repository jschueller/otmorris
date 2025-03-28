#!/usr/bin/env python

import openturns as ot
import openturns.testing as ott
import otmorris
import time

f = ot.Function(otmorris.MorrisFunction())
dim = f.getInputDimension()
x1 = [0.3] * dim
x2 = [0.4] * dim
x3 = [0.5] * dim
y1 = f(x1)
y2 = f(x2)
y3 = f(x3)
print(y1, y2, y3)
ott.assert_almost_equal(y1, [-17.738])
ott.assert_almost_equal(y2, [19.2912])
ott.assert_almost_equal(y3, [50])

X = ot.Normal([0.4] * dim, [0.1] * dim, ot.CorrelationMatrix(dim))
N = 1000
x = X.getSample(N)
t0 = time.time()
y = f(x)
t1 = time.time()
print(N / (t1 - t0), "eval/s")
print(y)


inputs = list(ot.Description.BuildDefault(dim, "x")) + list(ot.Description.BuildDefault(10, "a"))
formula = """
var X[20] := {x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19};
w = (X - [0.5] * 20) * 2
var w[X[]] := [ 2x - 1 ];
for (var k:=2; k<=6; k+=2) {w[k] = 2.0 * (1.1 * X[k] / (X[k] + 0.1) - 0.5)};
var b1[20] := {20, 20, 20, 20, 20, 20, 20, 20, 20, 20};
var y:= sum(w * b1);
for (var i:=2; i<=6; i+=2) { for (var i:=2; i<=6; i+=2) { w[k] = 2.0 * (1.1 * X[k] / (X[k] + 0.1) - 0.5) } };
y
"""
f2 = ot.SymbolicFunction(inputs, formula)
