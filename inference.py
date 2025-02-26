import tensorflow as tf
import sys
import labelreg.helpers as helper
import labelreg.networks as network
import labelreg.apps as app
import os
from time import*


begin_time = time()
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "3"

# 0 - get configs
config = helper.ConfigParser(sys.argv, 'inference')

# 1 - images to register
reader_moving_image, reader_fixed_image, _, _ = helper.get_data_readers(config['Inference']['dir_moving_image'],
                                                                        config['Inference']['dir_fixed_image'])

# 2 - graph
# network for predicting ddf only
tf.compat.v1.disable_eager_execution()
ph_moving_image = tf.compat.v1.placeholder(tf.float32, [reader_moving_image.num_data]+reader_moving_image.data_shape+[1])
ph_fixed_image = tf.compat.v1.placeholder(tf.float32, [reader_fixed_image.num_data] + reader_fixed_image.data_shape + [1])

reg_net = network.build_network(network_type=config['Network']['network_type'],
                                minibatch_size=reader_moving_image.num_data,
                                image_moving=ph_moving_image,
                                image_fixed=ph_fixed_image)

# restore the trained weights
saver = tf.compat.v1.train.Saver()
sess = tf.compat.v1.Session()
saver.restore(sess, config['Inference']['file_model_saved'])


# 3 - compute ddf
testFeed = {ph_moving_image: reader_moving_image.get_data_moving_jdm(),
            ph_fixed_image: reader_fixed_image.get_data_fixed()}
ddf = sess.run(reg_net.ddf, feed_dict=testFeed)

helper.write_images(ddf, config['Inference']['dir_save'], 'ddf')

# warp the test images
warped_images = app.warp_volumes_by_ddf(reader_moving_image.get_data_moving_jdm()
                                        , ddf)
helper.write_images(warped_images, config['Inference']['dir_save'], 'warped_image')

# warp test labels of gland segmentation, i.e. label_indices=0
if config['Inference']['dir_moving_label']:
    # data_moving_label
    data_moving_label = helper.DataReader(config['Inference']['dir_moving_label']).get_data_moving_jdm(label_indices=[0])
    warped_labels = app.warp_volumes_by_ddf(data_moving_label, ddf)
    helper.write_images(warped_labels, config['Inference']['dir_save'], 'warped_label')
sess.close()

end_time = time()
run_time = end_time-begin_time
print("----- Test Over -----")
print('Time：', run_time)