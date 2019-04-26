import requests
import config
import json
import process
import log
import os
import time
import codecs


def get_task():
    param_path = config.CONFIG_FILE
    with open(param_path, 'r') as f:
        param = json.load(f)
    return param


def send_task(url, param):
    data = {
        "para": json.dumps(param)
    }
    print(data)
    response = requests.post(url=url, data=data)
    result = response.json()
    print("send task: " + str(result))
    return result


def get_task_status(url, taskID):
    para = {"taskID": taskID}
    data = {
        "para": json.dumps(para)
    }
    print(data)
    response = requests.post(url=url, data=data)
    result = response.json()
    print("get task status: " + str(result))
    return result


def send_task_status():
    pass


def get_task_result():
    pass


def send_task_result():
    pass


def write_result(content, task_id):
    with codecs.open(os.path.join(config.RESULT_FILE, str(task_id) + '.result'), 'w', 'utf-8') as f:
        json.dump(content, f, ensure_ascii=False)


if __name__ == '__main__':
    log.task_start()
    try:
        os.makedirs(config.LOG_FILE)
    except Exception as e:
        pass
    try:
        os.makedirs(config.RESULT_FILE)
        # write_result({"machineid": 0, "progress": 0, "state": "DL_WAIT", "djid": 659}, "659") # for test
    except Exception as e:
        pass

    log.get_conf()
    try:
        param = get_task()
        task_id = param["taskID"]
        log.get_conf_success()

        process = process.processManager()
        process.set_taskid(task_id, task_id)
        send_task(config.SEND_TASK_ADDRESS, param)

        log.task_run()
        finished_tasks = []
        while True:

            callback = get_task_status(config.GET_TASK_STATUS_ADDRESS, task_id)
            results = json.loads(callback['callback'])

            # cheche the task's status
            task_status = results['result']['compeletestate']
            if task_status == 1:
                # get job's storage path
                tasks = results['result']['tasks']
                content = {
                    "taskID": task_id,
                    "tasks": []
                }
                for task in tasks:
                    content["tasks"].append(task)
                    log.write_result()
                    try:
                        write_result(content, task_id)
                        log.write_result_success()
                    except Exception as e:
                        print("write result err: " + str(e))
                        log.write_result_fail()
                process.resultCreate()
                print("sending...")
                process.final_send()
                break
            else:
                time.sleep(15)

            # tasks = results['result']['tasks']
            # task_num = len(tasks)
            # print("finished_tasks: " + str(len(finished_tasks)))
            # print("task_num: " + str(task_num))
            #
            # for task in tasks:
            #     state = task['state']
            #     if (state == "DL_SUCCESS" or state == "DL_FAIL") and task not in finished_tasks:
            #         finished_tasks.append(task)
            #         process.resultCreate()
            #
            #         if state == "DL_SUCCESS":
            #             log.write_result()
            #             djid = task["djid"]
            #             try:
            #                 write_result(task, djid)
            #                 log.write_result_success()
            #             except Exception as e:
            #                 log.write_result_fail()
            #
            #
            # if len(finished_tasks) == task_num:
            #     break

    except Exception as e:
        print(e)
        log.get_conf_fail()
