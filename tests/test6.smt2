(set-info :smt-lib-version 2.6)
(set-logic QF_UF)
(set-info :source |Benchmarks from the paper: "Extending Sledgehammer with SMT Solvers" by Jasmin Blanchette, Sascha Bohme, and Lawrence C. Paulson, CADE 2011.  Translated to SMT2 by Andrew Reynolds and Morgan Deters.|)
(set-info :category "industrial")
(set-info :status unsat)
(declare-sort S1 0)
(declare-fun f (S1) S1)
(declare-fun x () S1)
(declare-fun y () S1)
(assert (= (f x) (f y)))
(assert (not (= x y)))
(check-sat)
(exit)
