import copy


# function used to read the txt file and return a list of file's contents
def read_file() -> list:
    # open file
    admission_data = open("applicant_list.txt", mode='r+')
    # admission_data = open("applicant_list_test.txt", mode='r+')
    # init student list
    student_list = []
    for line in admission_data:
        # read name, last name and GPA into student list
        student_list.append(line.split())
    return student_list


# big function used to perform all student processing and return a dict with processed values
def process_students(student_list: list, max_no_of_apps: int) -> dict:
    # rest of students
    not_accepted = []
    # # sort student list NOT NEEDED NOW
    # sorted_student_list = sorted(student_list, key=lambda x: (-float(x[2]), ' '.join([x[0], x[1]])))
    sorted_student_dict = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}
    # refill dict according to student interest, value[7] being student's first choice
    for counter, key in enumerate(sorted_student_dict.keys()):
        for inner_counter, value in enumerate(student_list):
            if key == value[7]:
                sorted_student_dict[key].append(value)
    # sort applicants according to max of either average of exam score, or special admission test score
    for counter, key in enumerate(sorted_student_dict.keys()):
        if key == 'Biotech':  # x[3] + x[2] / 2 being chemistry and physics avg result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[3]) + float(x[2])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Chemistry':  # x[3] being chemistry result
            sorted_student_dict[key] = sorted(sorted_student_dict[key],
                                              key=lambda x: (-max(float(x[3]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Engineering':  # x[5] + x[4]  being computer science and math avg result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[5]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Mathematics':  # x[4] being math result
            sorted_student_dict[key] = sorted(sorted_student_dict[key],
                                              key=lambda x: (-max(float(x[4]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Physics':  # x[2] + x[4] being physics and math avg result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[2]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
    # now check for max no of applicants and separate not accepted applicants from accepted aplicants
    for counter, key in enumerate(sorted_student_dict.keys()):
        if len(sorted_student_dict[key]) > max_no_of_apps:
            # not accepted applicants
            not_accepted.append(sorted_student_dict[key][max_no_of_apps:])
            # update dict with max no of applicants
            sorted_student_dict[key] = sorted_student_dict[key][:max_no_of_apps]
    # flatten not accepted, cool way of flattening a list
    not_accepted = sum(not_accepted, [])
    # create a copy of not accepted list to be used in the 2nd round
    not_accepted_2nd = copy.deepcopy(not_accepted)
    # now check if some departments accepted less than maximum number of students
    # for those departments we will have 2nd round, and 3rd and so on
    for counter, key in enumerate(sorted_student_dict.keys()):
        # now we need to sort students by max of average scores, or admission score
        # but only for department in question, we do this dynamically
        if key == 'Biotech':
            dynamic_sort = sorted(not_accepted, key=lambda x: (
            -max(((float(x[3]) + float(x[2])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Chemistry':
            dynamic_sort = sorted(not_accepted, key=lambda x: (-max(float(x[3]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Engineering':
            dynamic_sort = sorted(not_accepted, key=lambda x: (
            -max(((float(x[5]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Mathematics':
            dynamic_sort = sorted(not_accepted, key=lambda x: (-max(float(x[4]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Physics':
            dynamic_sort = sorted(not_accepted, key=lambda x: (
            -max(((float(x[2]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        for inner_counter, value in enumerate(dynamic_sort):
            # loop through each departments not accepted candidates
            if len(sorted_student_dict[key]) < max_no_of_apps and key == value[8]:  # 2nd round is value[8]
                # print(f"2nd round start ! for {key} department")
                sorted_student_dict[key].append(value)
                # update not accepted candidate list by removing accepted candidates from the 2nd round
                not_accepted_2nd.remove(value)
    # create a copy of not accepted candidates from the 2nd round, to be used in 3rd round
    not_accepted_3rd = copy.deepcopy(not_accepted_2nd)
    # repeat the same for 3rd round, now iterate through not accepted candidates from the 2nd round
    for counter, key in enumerate(sorted_student_dict.keys()):
        # now we need to sort students by max of average scores, or admission score
        # but only for department in question, we do this dynamically
        if key == 'Biotech':  # NOTICE NOT_ACCPETED_2ND LIST HERE, WE SORT THAT LIST
            dynamic_sort3 = sorted(not_accepted_2nd, key=lambda x: (
            -max(((float(x[3]) + float(x[2])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Chemistry':
            dynamic_sort3 = sorted(not_accepted_2nd,
                                   key=lambda x: (-max(float(x[3]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Engineering':
            dynamic_sort3 = sorted(not_accepted_2nd, key=lambda x: (
            -max(((float(x[5]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Mathematics':
            dynamic_sort3 = sorted(not_accepted_2nd,
                                   key=lambda x: (-max(float(x[4]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Physics':
            dynamic_sort3 = sorted(not_accepted_2nd, key=lambda x: (
            -max(((float(x[2]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        for inner_counter, value in enumerate(dynamic_sort3):
            # loop through each departments not accepted candidates
            if len(sorted_student_dict[key]) < max_no_of_apps and key == value[9]:  # 3rd round is value[9]
                # print(f"3rd round start ! for {key} department")
                sorted_student_dict[key].append(value)
                # print(value)
                # update not accepted candidate list by removing accepted candidates from the 2nd round
                not_accepted_3rd.remove(value)
    # now do the final sorting of applicants according to test results (and name)
    for counter, key in enumerate(sorted_student_dict.keys()):
        if key == 'Biotech':  # x[3] being chemistry result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[3]) + float(x[2])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Chemistry':  # x[3] being chemistry result
            sorted_student_dict[key] = sorted(sorted_student_dict[key],
                                              key=lambda x: (-max(float(x[3]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Engineering':  # x[5] being computer science result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[5]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Mathematics':  # x[4] being math result
            sorted_student_dict[key] = sorted(sorted_student_dict[key],
                                              key=lambda x: (-max(float(x[4]), float(x[6])), ' '.join([x[0], x[1]])))
        if key == 'Physics':  # x[2] being physics result
            sorted_student_dict[key] = sorted(sorted_student_dict[key], key=lambda x: (
            -max(((float(x[2]) + float(x[4])) / 2), float(x[6])), ' '.join([x[0], x[1]])))
    return sorted_student_dict


def run():
    # ask the user for max number of applicants per department
    max_no_of_applicants = int(input())
    # max_no_of_applicants = 2 #used for testing
    student_list = read_file()
    # print(student_list)
    sorted_student_dict = process_students(student_list=student_list, max_no_of_apps=max_no_of_applicants)
    # create new files if they dont exist
    biotech_file = open("biotech.txt", 'w+', encoding='utf-8')
    chem_file = open("chemistry.txt", 'w+', encoding='utf-8')
    eng_file = open("engineering.txt", 'w+', encoding='utf-8')
    phys_file = open("physics.txt", 'w+', encoding='utf-8')
    math_file = open("mathematics.txt", 'w+', encoding='utf-8')
    for key, value in sorted_student_dict.items():
        print('\n', key)
        for counter, item in enumerate(value):
            # print(item)
            # now print correct score for each department
            if key == 'Biotech':
                print(' '.join(item[0:2]), str(max(((float(item[3]) + float(item[2])) / 2), float(item[6]))))
                # print(item)
                biotech_file.write(str(' '.join(item[0:2])) + ' ' + str(
                    max(((float(item[3]) + float(item[2])) / 2), float(item[6]))) + '\n')
            if key == 'Chemistry':
                print(' '.join(item[0:2]), str(max(float(item[3]), float(item[6]))))
                # print(item)
                chem_file.write(str(' '.join(item[0:2])) + ' ' + str(max(float(item[3]), float(item[6]))) + '\n')
            if key == 'Engineering':
                print(' '.join(item[0:2]), str(max(((float(item[4]) + float(item[5])) / 2), float(item[6]))))
                # print(item)
                eng_file.write(str(' '.join(item[0:2])) + ' ' + str(
                    max(((float(item[4]) + float(item[5])) / 2), float(item[6]))) + '\n')
            if key == 'Physics':
                print(' '.join(item[0:2]), str(max(((float(item[2]) + float(item[4])) / 2), float(item[6]))))
                # print(item)
                phys_file.write(str(' '.join(item[0:2])) + ' ' + str(
                    max(((float(item[2]) + float(item[4])) / 2), float(item[6]))) + '\n')
            if key == 'Mathematics':
                print(' '.join(item[0:2]), str(max(float(item[4]), float(item[6]))))
                # print(item)
                math_file.write(str(' '.join(item[0:2])) + ' ' + str(max(float(item[4]), float(item[6]))) + '\n')
    # close files
    biotech_file.close()
    chem_file.close()
    eng_file.close()
    phys_file.close()
    math_file.close()


if __name__ == '__main__':
    run()
# # STAGE 7-FINAL STAGE-END
