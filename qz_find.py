

def second_third_avg(a, b, c, d):#返回值为中间俩个数的平均值
    numbers = [a, b, c, d]
    numbers.sort(reverse=True)
    second = numbers[1]
    third = numbers[2]
    return (second + third) / 2
def check_conditions(a, b, c, d):
    diff = a - b
    if diff > c:
        return 1
    elif diff < d:
        return 2
    else:
        return 0
def calculate_QiZi(img, ROI1, ROI1_1, ROI1_2, ROI1_3, ROI1_4,threshold_high,threshold_low):

    stats = img.get_statistics(roi=ROI1)
    l_avg = stats.l_mean()
    stats = img.get_statistics(roi=ROI1_1)
    l_avg_1 = stats.l_mean()
    stats = img.get_statistics(roi=ROI1_2)
    l_avg_2 = stats.l_mean()
    stats = img.get_statistics(roi=ROI1_3)
    l_avg_3 = stats.l_mean()
    stats = img.get_statistics(roi=ROI1_4)
    l_avg_4 = stats.l_mean()
    l_avg_avg = second_third_avg(l_avg_1, l_avg_2, l_avg_3, l_avg_4)
    # print(l_avg-l_avg_avg)
    QiZi1_1 = check_conditions(l_avg, l_avg_avg, threshold_high, threshold_low)
    return QiZi1_1


ROI_All=(1,1,319,239)
ROI1 = (84, 15, 30, 32)
ROI1_1 = (112, 47, 15, 14)
ROI1_2 = (65, 46, 10, 14)
ROI1_3 = (115, 2, 15, 10)
ROI1_4 = (70, 1, 13, 12)
ROI2 = (153, 15, 34, 36)
ROI2_1 = (138, 1, 13, 11)
ROI2_2 = (187, 4, 13, 10)
ROI2_3 = (134, 48, 15, 15)
ROI2_4 = (186, 51, 14, 14)
ROI3 = (223, 24, 31, 30)
ROI3_1 = (256, 55, 13, 15)
ROI3_2 = (209, 51, 13, 15)
ROI3_3 = (210, 5, 12, 12)
ROI3_4 = (256, 12, 10, 10)
ROI4 = (75, 82, 35, 39)
ROI4_1 = (110, 120, 14, 15)
ROI4_2 = (62, 119, 13, 14)
ROI4_3 = (64, 68, 12, 14)
ROI4_4 = (112, 68, 15, 13)
ROI5 = (147, 84, 36, 39)
ROI5_1 = (184, 123, 13, 16)
ROI5_2 = (131, 119, 12, 17)
ROI5_3 = (134, 69, 11, 17)
ROI5_4 = (185, 71, 14, 13)
ROI6 = (221, 87, 32, 40)
ROI6_1 = (206, 123, 11, 15)
ROI6_2 = (255, 126, 11, 14)
ROI6_3 = (208, 72, 13, 19)
ROI6_4 = (255, 77, 13, 10)
ROI7 = (75, 153, 33, 35)
ROI7_1 = (108, 190, 14, 14)
ROI7_2 = (64, 187, 9, 12)
ROI7_3 = (62, 141, 12, 12)
ROI7_4 = (108, 144, 14, 12)
ROI8 = (145, 157, 34, 38)
ROI8_1 = (180, 194, 14, 13)
ROI8_2 = (130, 192, 15, 11)
ROI8_3 = (131, 144, 13, 15)
ROI8_4 = (180, 146, 15, 10)
ROI9 = (221, 159, 26, 36)
ROI9_1 = (249, 195, 10, 12)
ROI9_2 = (201, 191, 12, 16)
ROI9_3 = (204, 146, 12, 13)
ROI9_4 = (253, 146, 12, 13)
QiZi1_1=0
QiZi1_2=0
QiZi1_3=0
QiZi2_1=0
QiZi2_2=0
QiZi2_3=0
QiZi3_1=0
QiZi3_2=0
QiZi3_3=0



