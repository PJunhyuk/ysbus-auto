#-*- coding: utf-8 -*-

from selenium import webdriver

import datetime
import time

import argparse

def main(args):

    ## Get bus_target_list from args
    ## bus_target: string to list

    bus_target_list = args.bus_target.split(',')

    print("TARGET!")

    for i in range(len(bus_target_list)):
        bus_target_args = bus_target_list[i].split('_')

        target_date_year = int(bus_target_args[0][0:4])
        target_date_month = int(bus_target_args[0][4:6])
        target_date_day = int(bus_target_args[0][6:8])

        target_date = datetime.date(target_date_year, target_date_month, target_date_day)
        target_day = '일'
        if target_date.weekday() == 0: target_day = '월'
        elif target_date.weekday() == 1: target_day = '화'
        elif target_date.weekday() == 2: target_day = '수'
        elif target_date.weekday() == 3: target_day = '목'
        elif target_date.weekday() == 4: target_day = '금'

        target_way = 0
        if bus_target_args[1] == 'STG':
            target_way = 1
        elif bus_target_args[1] == 'GTS':
            target_way = 2

        target_bus = bus_target_args[2]

        if target_way == 1:
            if bus_target_args[2] == '0720':
                target_bus = 1
            elif bus_target_args[2] == '0750':
                target_bus = 3
            elif bus_target_args[2] == '0830':
                target_bus = 4
            elif bus_target_args[2] == '0930':
                target_bus = 5
            elif bus_target_args[2] == '1030':
                target_bus = 6
            elif bus_target_args[2] == '1130':
                target_bus = 7
            elif bus_target_args[2] == '1230':
                target_bus = 9
            elif bus_target_args[2] == '1430':
                target_bus = 10
            elif bus_target_args[2] == '1500':
                target_bus = 11
            elif bus_target_args[2] == '1630':
                target_bus = 12
            elif bus_target_args[2] == '1730':
                target_bus = 14
            elif bus_target_args[2] == '1800':
                target_bus = 15
            elif bus_target_args[2] == '1830':
                target_bus = 16
            elif bus_target_args[2] == '1900':
                target_bus = 17
            elif bus_target_args[2] == '2000':
                target_bus = 18
            elif bus_target_args[2] == '2100':
                target_bus = 19
            else:
                print(bus_target_list[i] + ': hour ERROR')
                break
        else:
            if bus_target_args[2] == '0720':
                target_bus = 1
            elif bus_target_args[2] == '0740':
                target_bus = 2
            elif bus_target_args[2] == '0830':
                target_bus = 3
            elif bus_target_args[2] == '0930':
                target_bus = 4
            elif bus_target_args[2] == '1030':
                target_bus = 6
            elif bus_target_args[2] == '1130':
                target_bus = 7
            elif bus_target_args[2] == '1230':
                target_bus = 8
            elif bus_target_args[2] == '1430':
                target_bus = 9
            elif bus_target_args[2] == '1530':
                target_bus = 11
            elif bus_target_args[2] == '1630':
                target_bus = 12
            elif bus_target_args[2] == '1700':
                target_bus = 13
            elif bus_target_args[2] == '1730':
                target_bus = 14
            elif bus_target_args[2] == '1800':
                target_bus = 15
            elif bus_target_args[2] == '1815':
                target_bus = 16
            elif bus_target_args[2] == '1830':
                target_bus = 17
            elif bus_target_args[2] == '1930':
                target_bus = 19
            else:
                print(bus_target_list[i] + ': hour ERROR')
                break

        ## ASSERT CHECK

        if target_way == 1:
            target_way_print = '신촌발 국캠행'
        else:
            target_way_print = '국캠발 신촌행'

        print(target_date, '(', target_day, ')', target_way_print, '-', bus_target_args[2])


    while(1):

        # 10초에 한 번씩 체크
        time.sleep(10)

        for i in range(len(bus_target_list)):

            bus_target_args = bus_target_list[i].split('_')

            target_date_year = int(bus_target_args[0][0:4])
            target_date_month = int(bus_target_args[0][4:6])
            target_date_day = int(bus_target_args[0][6:8])

            target_date = datetime.date(target_date_year, target_date_month, target_date_day)

            # check today's date VS target_list
            if target_date.toordinal() - 2 == datetime.datetime.now().toordinal(): ## Lets book it!

                if datetime.datetime.now().hour == 14:

                    ## chromedriver
                    driver = webdriver.Chrome('./chromedriver')
                    driver.implicitly_wait(1)
                    driver.get('https://ysweb.yonsei.ac.kr/ysbus.jsp')

                    # 아이디 비밀번호 입력
                    driver.find_element_by_name('userid').send_keys(args.user_id)
                    driver.find_element_by_name('password').send_keys(args.user_pw)

                    # 로그인 버튼 클릭
                    driver.find_element_by_xpath('/html/body/div/div/div/div/form//h3/a').click()

                    #### 로그인 완료!

                    # 예약 페이지로 이동
                    driver.get('https://ysweb.yonsei.ac.kr/busTest/index2.jsp')

                    # 방향 설정
                    if target_way == 2:
                        driver.find_element_by_css_selector('.ty2 li:nth-child(2) a').click()
                    else:
                        driver.find_element_by_css_selector('.ty2 li:nth-child(1) a').click()

                    # 날짜 설정
                    el = driver.find_element_by_id('selectedDate')
                    for option in el.find_elements_by_tag_name('option'):
                        if target_day in option.text:
                            option.click()
                            break

                    # 예약사유 설정
                    el = driver.find_element_by_css_selector('table.display tr:nth-child(' + str(target_bus) + ') .selectedReason')
                    for option in el.find_elements_by_tag_name('option'):
                        if args.bus_reason in option.text:
                            option.click()
                            break

                    # 신청 버튼 클릭
                    driver.find_element_by_css_selector('table.display tr:nth-child(' + str(target_bus) + ') td:last-child a').click()

                    # alert 창 확인
                    driver.switch_to_alert().accept()

                    print(target_date, '(', target_day, ')', target_way_print, '-', bus_target_args[2], '완료!')
                    print(datetime.datetime.now())

                    del bus_target_list[i]

                    driver.quit()

        print('listening... ' + str(datetime.datetime.now()))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--user_id', type=str, help='student ID', required=True)
    parser.add_argument('--user_pw', type=str, help='portal PW', required=True)

    parser.add_argument('--bus_target', type=str, help='target', required=True)
    # 20180903_STG_09,20180903_GTS_01

    parser.add_argument('--bus_reason', type=str, default='강의', help='reason')

    args = parser.parse_args()
    # print(args)

    main(args)
