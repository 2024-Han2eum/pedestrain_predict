import csv
import cv2

def cluster_points(data_points, frame, spline_id):
    current_points = []
    previous_points = []
    next_points = []

    for x, y, f, s_id in data_points:
        if f == frame and s_id == spline_id:
            current_points.append((x, y))
        elif f < frame and s_id == spline_id:
            previous_points.append((x, y))
        elif f > frame and s_id == spline_id:
            next_points.append((x, y))

    return current_points, previous_points, next_points

if __name__ == "__main__":
    # 데이터셋 파일 경로
    csv_path = r"C:/Users/akiza/PycharmProjects/crowds/data/temporary_spline_data.csv"

    # 비디오 파일 경로
    video_path = r"C:/Users/akiza/PycharmProjects/crowds/data/crowds_zara01.avi"

    # 특정 프레임 선택
    target_frame = 100

    # READ CSV
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 헤더 행 스킵

        # CSV 파일의 각 행에서 x, y, frame 값을 읽어 리스트에 저장
        data_points = [(float(row[0]), float(row[1]), int(row[2]), int(row[3])) for row in csvreader]

    # RUN VIDEO
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        while True:
            ret, img = cap.read()

            if ret:  # 프레임 읽기 정상
                # 프레임별 좌표 찾기
                for spline_id in range(1, 11):  # 스플라인 ID는 1부터 10까지 있음
                    current_points, previous_points, next_points = cluster_points(data_points, target_frame, spline_id)

                    # 이전 점들 선으로 연결
                    if previous_points:
                        for i in range(1, len(previous_points)):
                            cv2.line(img, (int(previous_points[i - 1][0] + 720/2), int(576 - previous_points[i - 1][1] - 576/2)),
                                     (int(previous_points[i][0] + 720/2), int(576 - previous_points[i][1] - 576/2)),
                                     color=(255, 0, 0), thickness=2)

                    # 이후 점들 선으로 연결
                    if next_points:
                        for i in range(1, len(next_points)):
                            cv2.line(img, (int(next_points[i - 1][0] + 720/2), int(576 - next_points[i - 1][1] - 576/2)),
                                     (int(next_points[i][0] + 720/2), int(576 - next_points[i][1] - 576/2)),
                                     color=(0, 255, 0), thickness=2)

                    # 현재 점들 원으로 표시
                    for x, y in current_points:
                        x1 = int(x + 720/2)
                        y1 = int(576 - y - 576/2)
                        img = cv2.circle(img, (x1, y1), radius=5, color=(0, 0, 255), thickness=-1)

                cv2.imshow(video_path, img)  # 화면에 표시


                cv2.waitKey(0)  # 키 입력 대기

                break  # target_frame에 해당하는 프레임을 처리하고 종료합니다.
            else:
                print("can't read video frame.")
                break
    else:
        print("can't open video.")
    cap.release()
    cv2.destroyAllWindows()
