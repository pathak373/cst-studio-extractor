def dataExtractor(gain_file: str, s11_file: str, save_file: str, gain_split: int, s11_split):

    import csv

    def extractParams(temp) -> dict:
        params = temp[:1][0][0]
        temp = temp[3:]

        params = params.split("; ")

        final_params = {
            
        }

        params[0] = params[0][15:]
        params[-1] = params[-1][:-1]

        for param in params:
            x, y = param.split("=")
            final_params[str(x)] = float(y)

        return final_params

    def extractMin(temp) -> tuple:
        frequencies = []
        values = []

        for item in temp:
            item = item[0]
            freq, val = item.split("\t")
            freq, val = float(freq), float(val)
            frequencies.append(freq)
            values.append(val)

        freq = frequencies[values.index(min(values))]
        min_return_loss = min(values)

        return (freq, min_return_loss)

    def freqVsGain():

        PER_VAL = gain_split

        with open(gain_file, 'r') as file:
            reader = csv.reader(file)

            frequencies_lst = []
            gain_lst = []
            data = []

            for i in reader:
                data.append(i)        

            while data != []:
                temp = data[:PER_VAL]
                final_params = extractParams(temp)
                temp = temp[3:]
                frequencies = []
                values = []

                for item in temp:
                    item = item[0]
                    freq, val = item.split("\t")
                    freq, val = float(freq), float(val)
                    frequencies.append(freq)
                    values.append(val)
            
                data = data[PER_VAL:] 
                frequencies_lst.append(frequencies)
                gain_lst.append(values)
        
        return frequencies_lst, gain_lst

    def minS11():

        final_params_lst = []
        minimum_lst = []
        PER_VAL = s11_split

        with open(s11_file, 'r') as file:
            reader = csv.reader(file)
            data = []

            for i in reader:
                data.append(i)        

            while data != []:
                temp = data[:PER_VAL]
                final_params = extractParams(temp)
                temp = temp[3:]
                minimum = extractMin(temp)
                data = data[PER_VAL:]
                final_params_lst.append(final_params)
                minimum_lst.append(minimum) 

        return final_params_lst, minimum_lst

    # MINIMUM => (freq, return loss)
    final_params, minimum = minS11()
    frequencies_lst, gain_lst = freqVsGain()

    with open(save_file, 'w', newline="") as file:

        writer = csv.writer(file)

        header = []

        temp = final_params[0]
        for i, (key, value) in enumerate(temp.items()):
            header.append(key)

        header.append("freq")
        header.append("s11")
        header.append("gain")

        writer.writerow(header)

        for i in range(len(final_params)):
            params = final_params[i]
            minima = minimum[i]
            frequencies = frequencies_lst[i]
            gains = gain_lst[i]

            required_frequency = minima[0]

            for freq in frequencies:
                if freq == required_frequency:
                    gain = gains[frequencies.index(freq)]
                    break
                
                if freq > required_frequency:
                    j = frequencies.index(freq)

                    p1 = (frequencies[j - 0], gains[j - 0])
                    p2 = (frequencies[j - 1], gains[j - 1])

                    x1, y1 = p1[0], p1[1]
                    x2, y2 = p2[0], p2[1]

                    gain = y1 + ( (required_frequency - x1) * (y2 - y1) ) / (x2 - x1)

                    break

            load = []

            for i, (key, value) in enumerate(params.items()):
                load.append(value)

            load.append(required_frequency)
            load.append(minima[1])
            load.append(gain)

            writer.writerow(load)