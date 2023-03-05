def txt_extractor(content):
    ydata = []
    start_flag = False
    for line in content.split('\n'):
        if line=='':
            continue
        print(line)
        # print(type(line), line)
        # print(line.split())

        if start_flag:
            ydata.append(float(line.split()[3]))
        if line.startswith('time'):
            print(123)
            start_flag = True
    xdata = []
    for i in range(len(ydata)):
        xdata.append(round(0.05*i, 2))
    print(ydata)
    return xdata, ydata