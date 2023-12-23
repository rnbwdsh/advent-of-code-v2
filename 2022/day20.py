def test_20(data, level):
    mul = (811589153 if level else 1)
    nums = [(int(num_s) * mul, idx) for idx, num_s in enumerate(data)]  # adding index guarantees uniqueness

    for num in nums * (10 if level else 1):  # multiply creates a copy
        target = nums.index(num) + num[0]  # tuples are unique, to prevent errors on duplicates
        nums.remove(num)
        nums.insert(target % len(nums), num)

    i0 = [num[0] for num in nums].index(0)  # index of number 0
    return sum(nums[p % len(nums)][0] for p in range(1000 + i0, 4000 + i0, 1000))
