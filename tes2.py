import re

text = "SCT018"
pattern = r'((SCT|FEW|BKN|OVC)(\d{3})(CB)?)'

match = re.search(pattern, text)
if match:
    print("Match found:", match.group(0))