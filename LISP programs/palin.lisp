;; ===== PALINDROME =====
(defun string-reverse (s)
  (let* ((len (length s))
         (result (make-string len)))
    (dotimes (i len)
      (setf (char result i)
            (char s (- len 1 i))))
    result))

(defun palindrome-p (s)
  (string= s (string-reverse s)))

(defun run-palindrome ()
  (format t "Enter a word: ")
  (let* ((input (string (read)))
         (result (palindrome-p input)))
    (if result
      (format t "~a is a palindrome!~%" input)
      (format t "~a is NOT a palindrome.~%" input))))