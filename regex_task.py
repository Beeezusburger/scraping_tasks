import re


def capture_regex(pattern, text, is_inches=False):
    output = list()
    result = re.findall(pattern, text)
    if not result:
        return f'pattern {pattern} is not found in text {text}'
    for dimension in result[0]:
        if not isinstance(dimension, float):
            dimension = float(dimension.replace(',', '.'))
        if is_inches:
            dimension = dimension * 2.54
        output.append(round(dimension, 1))
    return output

print(
    capture_regex(r'(\d+)×(\d+)', '19×52cm'),
    capture_regex(r'(\d*)(?:\sx\s)(\d*\,?\d*)', '50 x 66,4 cm '),
    capture_regex(
        r'(\d*\.?\d*)(?:\sx\s)(\d*\.?\d*)(?:\sx\s)(\d*\.?\d*)\scm',
        '168.9 x 274.3 x 3.8 cm (66 1/2 x 108 x 1 1/2 in.)'
    ),
    capture_regex(
        r'(?:Image:.*)\((\d*\.?\d*)(?:\s\×\s)(\d*\.?\d*)\scm\)',
        'Sheet: 16 1/4 × 12 1/4 in. (41.3 × 31.1 cm) Image: 14 × 9 7/8 in. (35.6 × 25.1 cm)'
    ),
    capture_regex(r'(\d)(?:\sby\s)(\d)', '5 by 5in',is_inches=True)
)
