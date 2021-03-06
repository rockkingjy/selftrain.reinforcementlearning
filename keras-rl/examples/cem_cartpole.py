import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

ENV_NAME = 'CartPole-v0'


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)

nb_actions = env.action_space.n #action: 2
obs_dim = env.observation_space.shape[0] #obesrvation: 4
print env.observation_space.shape #(4,)

# Option 1 : Simple model
model = Sequential()
model.add(Dense(nb_actions,input_dim=obs_dim)) #param=4*2+2=10
model.add(Activation('softmax'))

# Option 2: deep network
# model = Sequential()
# model.add(Dense(16,input_dim=obs_dim))
# model.add(Activation('relu'))
# model.add(Dense(16))
# model.add(Activation('relu'))
# model.add(Dense(16))
# model.add(Activation('relu'))
# model.add(Dense(nb_actions))
# model.add(Activation('softmax'))

print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and even the metrics!
memory = EpisodeParameterMemory(limit=1000,max_episode_steps=200)

cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
               batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
cem.compile()

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
cem.fit(env, nb_steps=100000, visualize=False, verbose=2)

# After training is done, we save the best weights.
print("highest reward total seen : {0}".format(cem.best_seen[0]))
cem.model.set_weights(cem.get_weights_list(cem.best_seen[1]))
#cem.save_weights('cem_{}_params.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
cem.test(env, nb_episodes=5, visualize=True)
