from selenium import webdriver
import random
import time

sleep_time = 0
max_num_length = 5
driver = webdriver.Chrome(r"D:/selenium_chromedriver_win32/chromedriver.exe")

driver.maximize_window()
driver.get("http://localhost:4200/")


# calc_numbers = {int(num.get_property("value")): num for num in driver.find_elements_by_class_name("number")}
# # print(calc_numbers)
# calc_operators = {op.get_property("value"): op for op in driver.find_elements_by_class_name("operator")}
# # print(calc_operators)
# decimal = driver.find_element_by_class_name("decimal")
# print(type(decimal))
# equal = driver.find_element_by_class_name("equal-sign")
# # print(equal.get_property("value"))
# neg_operator = driver.find_element_by_class_name("neg_operator")
# # print(neg_operator.get_property("value"))


def simple_test(total_test_cases=10, with_decimal=False):
    calc_numbers = driver.find_elements_by_class_name("number")
    print("numbers", [int(num.get_property("value")) for num in calc_numbers])
    calc_operators = driver.find_elements_by_class_name("operator")
    print("operators", [op.get_property("value") for op in calc_operators])
    equal = driver.find_element_by_class_name("equal-sign")
    # print(equal.get_property("value"))
    decimal = driver.find_element_by_class_name("decimal")
    # print(type(decimal))
    neg_operator = driver.find_element_by_class_name("neg_operator")
    # print(neg_operator.get_property("value"))

    for _ in range(total_test_cases):
        num1 = ""
        num2 = ""
        num1_length = (random.randint(1, 1000) % max_num_length) + 1
        op_selection = random.randint(1, 1000) % 4
        num2_length = (random.randint(1, 1000) % max_num_length) + 1
        decimal_point_1 = -1
        decimal_point_2 = -1
        if with_decimal:
            decimal_point_1 = (random.randint(1, 1000) % max_num_length)
            decimal_point_2 = (random.randint(1, 1000) % max_num_length)

        # print(f"num1 {num1_length} digits long")
        # print(f"num2 {num2_length} digits long")

        for digit_pos in range(num1_length):
            if decimal_point_1 == digit_pos:
                num1 += "."
                decimal.click()
            n = random.randint(1, 1000) % 10
            # print(f"got {n}")
            # num1 = num1 * 10 + n
            num1 += str(n)
            # print(f"num1 {num1}")
            for num_ele in calc_numbers:
                if num_ele.get_property("value") == str(n):
                    num_ele.click()
                    # print(f"Clicked {num_ele.get_property('value')}")
                    break
            time.sleep(sleep_time)

        num1 = float(num1) if with_decimal else int(num1)

        time.sleep(sleep_time)
        selected_op = calc_operators[op_selection]
        selected_op.click()
        # print(f"Op clicked {selected_op.get_property('value')}")
        time.sleep(sleep_time)

        for digit_pos in range(num2_length):
            if decimal_point_2 == digit_pos:
                num2 += "."
                decimal.click()
            n = random.randint(1, 1000) % 10
            # print(f"got {n}")
            # num2 = num2 * 10 + n
            num2 += str(n)
            # print(f"num2 {num2}")
            for num_ele in calc_numbers:
                if num_ele.get_property("value") == str(n):
                    num_ele.click()
                    # print(f"Clicked {num_ele.get_property('value')}")
                    break
            time.sleep(sleep_time)

        num2 = float(num2) if with_decimal else int(num2)

        time.sleep(sleep_time)
        equal.click()
        result_received = driver.find_element_by_id("calculator-screen").get_property("value")
        result = 0
        if "+" == selected_op.get_property("value"):
            result = num1 + num2
        elif "-" == selected_op.get_property("value"):
            result = num1 - num2
        elif "*" == selected_op.get_property("value"):
            result = num1 * num2
        else:
            result = 0.0 if num2 == 0 else num1 / num2

        result = round(result, 2)
        result_received_in_float = -999999
        try:
            result_received_in_float = float(result_received)
        except ValueError as e:
            print(f"couldn't convert {result_received} to float.")

        print(num1, selected_op.get_property("value"), num2, "=", result, f", Received {result_received}",
              "pass" if result == result_received_in_float else "FAIL")

        assert str(result) in str(result_received_in_float)


# ttc = input("How many Test Cases want to run ? ")
# wd = input("Test Decimal point ? (0/1)")
simple_test(total_test_cases=50)
simple_test(total_test_cases=50, with_decimal=True)
print("Closing Driver.")
driver.close()
