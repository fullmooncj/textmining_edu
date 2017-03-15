from __future__ import print_function

import numpy as np
import tensorflow as tf

xy = np.loadtxt('news.target', unpack=True, dtype='float32')


x_data = np.transpose(xy[0:20])
y_data = np.transpose(xy[20:])


X = tf.placeholder("float", [None, 20])
Y = tf.placeholder("float", [None, 7])

W = tf.Variable(tf.zeros([20, 7]))

# matrix shape X=[8, 3], W=[3, 3]
hypothesis = tf.nn.softmax(tf.matmul(X, W))

learning_rate = 0.001

cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), reduction_indices=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    for step in range(2001):
        sess.run(optimizer, feed_dict={X: x_data, Y: y_data})
        if step % 200 == 0:
            print(step, sess.run(cost, feed_dict={X: x_data, Y: y_data}), sess.run(W))

    print('--------------------')
    print('global')
    a = sess.run(hypothesis, feed_dict={X: [[0.005917159763313609,    0.0,     0.011834319526627219,    0.0,     0.0,     0.0,     0.0,     0.0,     0.0,     0.005917159763313609,    0.0,     0.0,     0.0,     0.0,     0.0,    0.005917159763313609,    0.0,     0.0,     0.005917159763313609,    0.0]]})
    print(a, sess.run(tf.argmax(a, 1)))

    print('social')
    b = sess.run(hypothesis, feed_dict={X: [[0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.0,     0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666,    0.016666666666666666]]})
    print(b, sess.run(tf.argmax(b, 1)))

    print('politics')
    c = sess.run(hypothesis, feed_dict={X: [[0.045454545454545456,    0.045454545454545456,    0.0,     0.045454545454545456,    0.0,     0.0,     0.0,     0.0,     0.0,     0.045454545454545456,    0.0,     0.0,     0.0,     0.045454545454545456,    0.0,     0.0,     0.0,     0.045454545454545456,    0.045454545454545456,    0.0]]})
    print(c, sess.run(tf.argmax(c, 1)))

    #all = sess.run(hypothesis, feed_dict={X: [[1, 11, 7], [1, 3, 4], [1, 1, 0]]})
    #print(all, sess.run(tf.argmax(all, 1)))

