import numpy as np
import matplotlib.pyplot as plt

def logistic_function(x, fairness=1):
    # Logistic function for probability transformation
    return (1 / (1 + np.exp(-x)))**fairness

def weighted_logistic_prob(N, fairness=1):
    probabilities = np.array([logistic_function(-0.5 * (number - 1), fairness) for number in range(1, N + 1)])
    probabilities = probabilities / np.sum(probabilities)
    print('cek prob', probabilities)
    return probabilities

def weighted_logistic_random_choice(N, fairness=1):
    probabilities = np.array([logistic_function(-0.5 * (number - 1), fairness) for number in range(1, N + 1)])
    probabilities = probabilities / np.sum(probabilities)
    choice = np.arange(len(probabilities))
    choice += 1

    random_number = np.random.uniform()
    cumulative_probability = 0
    for i in range(len(probabilities)):
        probability = probabilities[i]
        cumulative_probability += probability
        chosen_number = choice[i]
        if random_number < cumulative_probability:
            break
    return chosen_number


N = 10
prob = weighted_logistic_prob(N, 4)

categories = np.arange(len(prob))
categories += 1

print('the choosen is', weighted_logistic_random_choice(N, 4))

plt.bar(categories, prob, color='blue')

# Adding labels and title
plt.xlabel('class')
plt.ylabel('Prob')
plt.title('prob distribution')

# Display the bar chart
plt.show()
