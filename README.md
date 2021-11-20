# Reisp

Reisp aims to be a statically typed version of Lisp

## Example

```lisp
(defn sum (a int b int) int
    (+ a b))

(defstruct Parser ()
    (source str
	index int))

(defn Parser.end () bool
	(>= index (len source)))

(defenum ParserErr ()
 	(InvalidOp
	 message str)
	(EOF
	 index int))

(defn main () void
	(let err (EOF 3)
	 (match err
	  (InvalidOp message
	   (print "Invalid operation!"))
	  (EOF index
	   (print "End of file!" index)))))
```

Reisp will be statically typed and checked before runtime. In addition, it also allows for better expressiveness with algebraic sum types and structs with methods.

*Note: this is still a work-in-progress language example*
