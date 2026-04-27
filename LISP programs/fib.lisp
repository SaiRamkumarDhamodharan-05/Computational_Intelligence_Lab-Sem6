;; ===== FIBONACCI =====
(defun fibonacci (n)
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (t (+ (fibonacci (- n 1))
          (fibonacci (- n 2))))))

(defun print-fibonacci (count)
  (dotimes (i count)
    (format t "~a " (fibonacci i)))
  (format t "~%"))

(defun run-fibonacci ()
  (format t "Enter no. of inputs: ")
  (let ((test-count (read)))
    (dotimes (i test-count)
      (let ((n (read)))
        (print-fibonacci n)))))