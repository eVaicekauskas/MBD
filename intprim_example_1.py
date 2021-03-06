import matplotlib.pyplot as plt
import numpy as np
import csv

# Import the library.
import intprim

from functions import *

plt.close('all')

# Set a seed for reproducibility
np.random.seed(213413414)

# Define some parameters used when generating synthetic data.
num_train_trajectories = 2#55#55#25
train_translation_mean = 0.15
train_translation_std = 0.5#1.0
train_noise_std = 0.02
train_length_mean = 55
train_length_std = 5#1#9

# Generate some synthetic handwriting trajectories.
training_trajectories = create_2d_data(
    num_train_trajectories,
    train_translation_mean,
    train_translation_std,
    train_noise_std,
    train_length_mean,
    train_length_std)

# Plot the results.
plt.figure()
for trajectory in training_trajectories:
    plt.plot(trajectory[0], trajectory[1])
plt.show()



# Define the data axis names.
dof_names = np.array(["X ", "Y "])

# Decompose the handwriting trajectories to a basis space with 8 uniformly distributed Gaussian functions and a variance of 0.1.
basis_model = intprim.basis.GaussianModel(10, 0.08, dof_names)
#basis_model = intprim.basis.SigmoidalModel(24, 0.08, dof_names)

domain = np.linspace(0, 1, training_trajectories[0].shape[1], dtype = intprim.constants.DTYPE)
weights = basis_model.fit_basis_functions_linear_closed_form(domain, training_trajectories[0].T).reshape(2, 10)
basis_model.plot_weighted(weights, dof_names)

# Initialize a BIP instance.
#primitive = intprim.BayesianInteractionPrimitive(basis_model)
primitive = intprim.BayesianInteractionPrimitive(basis_model)

# Train the model.
for trajectory in training_trajectories:
    primitive.add_demonstration(trajectory)

# Plot the distribution of the trained model.
mean, upper_bound, lower_bound = primitive.get_probability_distribution()
intprim.util.visualization.plot_distribution(dof_names, mean, upper_bound, lower_bound)



# Set an observation noise for the demonstrations.
#observation_noise = np.diag([10000.0, train_noise_std ** 2])
#observation_noise = np.diag([1.0, train_noise_std ** 2])
observation_noise = np.diag([1, 1])



# Compute the phase mean and phase velocities from the demonstrations.
phase_velocity_mean, phase_velocity_var = intprim.examples.get_phase_stats(training_trajectories)
mean_w, cov_w = primitive.get_basis_weight_parameters()
# Define a filter to use. Here we use an ensemble Kalman filter
filter = intprim.filter.spatiotemporal.ExtendedKalmanFilter(
    basis_model = basis_model,
    initial_phase_mean = [0.0, phase_velocity_mean],
    initial_phase_var = [1e-4, phase_velocity_var],
    proc_var = 1e-8,
    mean_basis_weights = mean_w,
    cov_basis_weights = cov_w)




#num_test_trajectories = 1
#test_translation_mean = 5.0
#test_translation_std = 1e-5
#test_noise_std = 0.01
#test_length_mean = 45
#test_length_std = 1e-5

# Create test trajectories.
#test_trajectories = create_2d_data(num_test_trajectories, test_translation_mean, test_translation_std, test_noise_std, test_length_mean, test_length_std)


dataFileID = '0'

while os.path.exists('samples/chairTest/lWristPoints_' + dataFileID + '.csv'):
    dataFileID = str(int(dataFileID)+1)

dataFileID = str(int(dataFileID)-1)

file = open('samples/chairTest/lWristPoints_' + dataFileID + '.csv')
csvreader = csv.reader(file)
rows = []
for row in csvreader:
    rows.append([-1*float(row[0]),float(row[1])])

file.close()

transpRows = np.transpose(rows)
#print(rows)

test_trajectories   = [np.array(transpRows)]

# Evaluate the trajectories.
#intprim.examples.evaluate_trajectories(primitive, filter, test_trajectories, observation_noise)
evaluate_trajectories(primitive, filter, test_trajectories, observation_noise)

