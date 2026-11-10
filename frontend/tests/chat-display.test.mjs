import test from "node:test";
import assert from "node:assert/strict";
import { appendStreamToken, getDistinctRelevantSchemes } from "../lib/chat/display.ts";

const scheme = (scheme_name, details = "scheme details") => ({ scheme_name, details });

test("streamed answer chunks appear once in the accumulated answer", () => {
  const chunks = ["The answer ", "continues here."];
  const answer = chunks.reduce(appendStreamToken, "");
  assert.equal(answer, "The answer continues here.");
  assert.equal(answer.split("The answer").length - 1, 1);
});

test("primary scheme is excluded from related cards, including name case differences", () => {
  const primary = scheme("Primary Scheme");
  const relevant = [scheme("primary scheme", "duplicate"), scheme("Different Scheme")];
  assert.deepEqual(getDistinctRelevantSchemes(primary, relevant), [relevant[1]]);
});

test("distinct relevant schemes still render alongside the primary scheme", () => {
  const primary = scheme("Primary Scheme");
  const relevant = [primary, scheme("First Scheme"), scheme("Second Scheme")];
  assert.deepEqual(getDistinctRelevantSchemes(primary, relevant), relevant.slice(1));
});
