;; ===== CIRCLE AREA =====
(defun circle-area (radius)
  (* pi radius radius))

(defun run-circle ()
  (format t "Enter radius: ")
  (let* ((r (read))
         (area (circle-area r)))
    (format t "Radius : ~a~%" r)
    (format t "Area   : ~,4f~%" area)))