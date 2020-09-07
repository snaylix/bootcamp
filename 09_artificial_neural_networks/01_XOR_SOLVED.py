input1 = float(input("enter first input  : "))
input2 = float(input("enter second input : "))

# Logical AND
w1 = [0.5, 0.5]
bias1 = 0
dot1 = input1 * w1[0] + input2 * w1[1] + bias1
out1 = 1.0 if dot1 > 0.5 else 0.0

print(out1)

# Logical OR
w2 = [0.5, 0.5]
bias2 = 0.5
dot2 = input1 * w2[0] + input2 * w2[1] + bias2
out2 = 1.0 if dot2 > 0.5 else 0.0

print(out2)

# 0 0
# 0 1
# 0 1
# 1 1

# Logical Exclusive OR
w3 = [-0.5, 0.5]
bias3 = 0.5
dot3 = out1 * w3[0] + out2 * w3[1] + bias3
out3 = 1.0 if dot3 > 0.5 else 0.0

print(out3)
