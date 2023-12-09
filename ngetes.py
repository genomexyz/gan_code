import re

# Sample TAF code
taf_code = "TAF WAFF 011100Z 0112/0200 33008KT 7000 SCT018 BECMG 0113/0115 35005KT TEMPO 0116/0119 30005KT 5000 RA BKN018 BECMG 0121/0123 00000KT 8000 SCT019="
taf_code = "TAF WAFF 011100Z 0112/0200 33008KT 7000 SCT018 BECMG 0113/0115 +RA BKN018CB="
taf_code = "TAF WAFF 132300Z 1400/1412 27005KT 8000 SCT020 BECMG 1402/1404 36015KT 9999 SCT020 TEMPO 1408/1412 27005KT 5000 -TSRA FEW017CB BKN020="
taf_code = "TAF WAFF 022300Z 0300/0312 VRB05KT 6000 SCT018 BECMG 0302/0305 33013KT 8000 SCT019 PROB40 TEMPO 0306/0309 VRB05KT 4000 -RA BKN016 TEMPO 0310/0312 6000 SCT017="
taf_code = "TAF WAFF 272300Z 2800/2812 14003KT 7000 FEW018CB BECMG 2803/2805 33008KT 6000 -TSRA TEMPO 2806/2809 34009KT 8000 SCT019="
taf_code = "TAF WAFF 241100Z 2412/2512 VRB05KT 8000 SCT019 PROB40 TEMPO 2417/2419 4000 -RA BKN018 BECMG 2503/2505 36015KT 9000 FEW020CB="

# Define a regex pattern to match TAF parameters
#pattern = r'TAF\s+(\w+)\s+(\d{6}Z)\s+(\d{4}/\d{4})\s+(\d{5}KT)\s+(\d{4})\s+(-?[A-Z]+)\s+(\w{3}\d{6}KT)\s+(\w{3}\d{6}KT)\s+(-?[A-Z]+)\s+(\w{2}\d{4})\s+(\w{3}\d{5}KT)\s+(-?[A-Z]+)\s+(\w{3}\d{5}KT)'
pattern = r'TAF\s+(\w{3}\s+)?(\w{4}\s+)(\d{6}Z\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT\s+)(\d{4}\s+)(([\+\-])?([A-Z]{2,5}\s+))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)(\d{4}/\d{4}\s+)((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?(PROB\d{2}\s+)?(BECMG\s+|TEMPO\s+)?(\d{4}/\d{4}\s+)?((VRB|\d{3})\d{2}KT(\s+|))?(\d{4}(\s+|))?(([\+\-]?[A-Z]{2,5})(\s+|))?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?\s+)?((SCT|FEW|BKN|OVC)(\d{3})(CB)?)?(=)'


# Use re.findall to extract parameters
matches = re.findall(pattern, taf_code)
print(matches)
exit()
# Print the extracted parameters
for match in matches:
    station = match[0]
    valid_time = match[1]
    forecast_time = match[2]
    wind = match[3]
    visibility = match[4]
    weather = match[5]
    fm_change1 = match[6]
    tempo_change1 = match[7]
    tempo_change2 = match[8]
    fm_change2 = match[9]

    print(f"Station: {station}")
    print(f"Valid Time: {valid_time}")
    print(f"Forecast Time: {forecast_time}")
    print(f"Wind: {wind}")
    print(f"Visibility: {visibility}")
    print(f"Weather: {weather}")
    print(f"FM Change 1: {fm_change1}")
    print(f"Tempo Change 1: {tempo_change1}")
    print(f"Tempo Change 2: {tempo_change2}")
    print(f"FM Change 2: {fm_change2}")

# You can access and manipulate these extracted parameters as needed for your aviation meteorology work.
