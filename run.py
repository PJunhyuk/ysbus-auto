from selenium import webdriver

import datetime

import argparse


def main(args):

    driver = webdriver.Chrome('./src/chromedriver')
    driver.get('https://ysweb.yonsei.ac.kr/ysbus.jsp')

    while(1):

        ## bus_target: string to list

        bus_target_list = args.bus_target.split(',')

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

            ## ASSERT CHECK

            print(target_date)
            print(target_day)
            print(target_way)
            print(target_bus)

            ## check today's date VS target_list

            if target_date.toordinal() - 2 == datetime.datetime.now().toordinal(): ## Lets book it!
                # if datetime.datetime.now().hour == 14:
                if datetime.datetime.now().hour:

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

                    print('완료!')
                    print(datetime.datetime.now())

                    del bus_target_list[i]




if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--user_id', type=str, help='student ID', required=True)
    parser.add_argument('--user_pw', type=str, help='portal PW', required=True)

    parser.add_argument('--bus_target', type=str, help='target', required=True)
    # 20180903_STG_09,20180903_GTS_01

    parser.add_argument('--bus_reason', type=str, default='강의', help='reason')

    args = parser.parse_args()
    print(args)

    main(args)