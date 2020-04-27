import cv2
import numpy as np
import os

frameInPageNum = 2

if __name__ == '__main__':
    cap = cv2.VideoCapture('C:/Users/xadxxadx/Downloads/Autumn Leaves.webm')
    if not os.path.exists('sheets'):
        os.mkdir('sheets')
    index = 0
    frame_list = []
    pre_frame = []
    frame = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        if pre_frame.__len__() == 0:
            frame_list.append(frame)
            cv2.imshow("test", frame)
            cv2.waitKey(0)
            pass
        else:
            _, mask1 = cv2.threshold(frame[:,:,1] - frame[:,:,0], 30, 255, cv2.THRESH_BINARY)
            _, mask2 = cv2.threshold(pre_frame[-1][:,:,1] - pre_frame[-1][:,:,1], 30, 255, cv2.THRESH_BINARY)
            mask = np.bitwise_or(mask1, mask2)
            #cv2.imshow("mask", mask)

            r = frame[:,:,0]
            r = cv2.bitwise_or(r, mask)
            r_pre = pre_frame[-1][:,:,0]
            r_pre = cv2.bitwise_or(r_pre, mask)
            diff = r.astype(np.float) - r_pre.astype(np.float)
            _, th = cv2.threshold(abs(diff), 10, 255, cv2.THRESH_BINARY)
            count = np.count_nonzero(th)
            print(str(count))
            if count > 30000:
                f_tmp = frame_list[-1]
                f_tmp[:, 0:int(f_tmp.shape[1]/2)] = pre_frame[0][:, 0:int(f_tmp.shape[1]/2)]
                frame_list[-1] = f_tmp
                frame_list.append(frame)
                cv2.imshow("pre", pre_frame[0])
                cv2.imshow("curr", frame)
                cv2.imshow("combime", f_tmp)
                cv2.waitKey(10)
                cv2.imwrite('sheets/' + str(index) + '.jpg', f_tmp)
                index+=1
        pre_frame.append(frame)
        if pre_frame.__len__() > 30:
            pre_frame.pop(0)
    f_tmp = frame_list[-1]
    f_tmp[:, 0:int(f_tmp.shape[1] / 2)] = pre_frame[0][:, 0:int(f_tmp.shape[1] / 2)]
    frame_list[-1] = f_tmp
    cv2.imwrite('sheets/' + str(index) + '.jpg', f_tmp)


    if not os.path.exists('sheetPage'):
        os.mkdir('sheetPage')

    page_Index = 0
    for index in range(0, frame_list.__len__(), 2):
        frame_up = frame_list[index]
        frame_bottom = frame_list[index+1]
        concated = cv2.vconcat([frame_up, frame_bottom])
        cv2.imwrite('sheetPage/' + str(page_Index) + '.jpg', concated)
        page_Index+=1


    pass
