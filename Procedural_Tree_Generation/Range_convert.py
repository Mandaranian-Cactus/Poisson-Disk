def convert_range(high, low, num):
    # Converts range into 0 - 1
    # Used ratios and sorta a property of similar triangles
    range = high - low
    return (num - low) / range
print(convert_range(0.6, 0.4, 0.5))
