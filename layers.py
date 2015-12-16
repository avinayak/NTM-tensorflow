import math
import tensorflow as tf

from utils import *

def Linear(inputs, output_size, stddev=0.5, bias=True, bias_init=0.0, name=None, mem_size=None):
    total_input_size = 0
    if type(inputs) != list:
        inputs = [inputs]
    shapes = [a.get_shape().as_list() for a in inputs]

    for shape in shapes:
        if len(shape) != 2:
            raise ValueError("Linear is expecting 2D inputuments: %s" % str(shapes))
        if not shape[1]:
            raise ValueError("Linear expects shape[1] of inputuments: %s" % str(shapes))
        else:
            total_input_size += shape[1]

    w_name = "%s_w" % name if name else None
    b_name = "%s_b" % name if name else None

    w = tf.identity(tf.random_normal([total_input_size, output_size], stddev=stddev, \
                                      name=w_name))
    if len(inputs) == 1:
      mul = tf.matmul(inputs[0], w)
    else:
      mul = tf.matmul(tf.concat(1, inputs), w)

    if bias:
        if mem_size:
            b = tf.Variable(tf.cast(tf.range(mem_size-2, 0, -1), dtype=tf.float32))
        else:
            b = tf.Variable(tf.constant(bias_init, shape=[output_size], dtype=tf.float32))
        return tf.nn.bias_add(mul, b)
    else:
        return mul

def SmoothCosineSimilarity(M_prev, k):
    M_dim_norm = tf.reshape(tf.sqrt(tf.reduce_sum(tf.mul(M_prev, M_prev),1)), [-1, 1])
    k_norm = tf.sqrt(tf.matmul(k, k, transpose_b=True))
    dot = tf.matmul(M_prev, k, transpose_b=True)
    similarity = tf.div(dot, (M_dim_norm * k_norm + 1e-3))
    return similarity

def ScalarMul(vector, beta):
    return vector * beta

def ScalarDiv(vector, beta):
    return vector / beta

def CircularConvolution(vector, kernel):
    size = int(vector.get_shape()[0])
    kernel_size = int(kernel.get_shape()[0])
    kernel_shift = int(math.floor(kernel_size/2.0))
    output = tf.Variable(tf.zeros_like(vector))

    def loop(idx):
        if idx < 0: return size + idx
        if idx >= size : return idx - size
        else: return idx

    for i in xrange(size):
        indices = [loop(i+j) for j in xrange(kernel_shift, -kernel_shift-1, -1)]
        v = tf.gather(vector, indices)
        output = tf.scatter_add(output, [i], tf.reduce_sum(v * kernel, 0, keep_dims=True))

    # # code with double loop
    # for i in xrange(size):
    #     for j in xrange(kernel_size):
    #         idx = i + kernel_shift - j + 1
    #         if idx < 0: idx = idx + size
    #         if idx >= size: idx = idx - size
    #         w = tf.gather(vector, int(idx)) * tf.gather(kernel, j)
    #         output = tf.scatter_add(output, [i], tf.reshape(w, [1, -1]))

    return output

def OuterProd(*inputs):
    order = len(inputs)
    if order == 2:
        output = tf.mul(inputs[0], inputs[1])
    elif order == 3:
        size = []
        idx = 1
        for i in xrange(order):
            size.append(inputs[i].get_shape()[0])
        output = tf.zeros(size)

        u, v, w = inputs[0], inputs[1], inputs[2]
        uv = tf.mul(inputs[0], inputs[1])
        for i in xrange(self.size[-1]):
            output = tf.scatter_add(output, [0,0,i], uv)

    return output
