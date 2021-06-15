import math


class Tracker:
    def __init__(self):
        self.points = {} #id,cx,cy,broj tikova
        self.id_count = 0

    def update(self, points):

        objects_bbs_ids = []

        #print('Centri koji su poslati', points)
        #print('Prethodno registrovani', self.points)
        for point in points:
            cx, cy = point

            min_distance = 1000
            object_detected = [-1, False]
            for ex_point_id, ex_point in self.points.items():
                dist = math.hypot(cx - ex_point[0], cy - ex_point[1])

                if dist < min_distance and dist < 25:
                    min_distance = dist
                    object_detected[1] = True
                    object_detected[0] = ex_point_id

            if object_detected[1]:
                _, _, cnt = self.points[object_detected[0]]
                cnt += 1
                self.points[object_detected[0]] = (cx, cy, cnt)
                objects_bbs_ids.append([cx, cy, object_detected[0]])

            else:
                self.points[self.id_count] = (cx, cy, 1)
                objects_bbs_ids.append([cx, cy, self.id_count])
                self.id_count += 1

        return objects_bbs_ids
