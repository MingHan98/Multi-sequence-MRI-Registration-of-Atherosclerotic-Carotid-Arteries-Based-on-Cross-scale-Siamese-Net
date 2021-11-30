import os
import nibabel as nib
import tensorflow as tf
import numpy as np
import apps

data_path_T1GD_label = r'C:\Users\Administrator\Desktop\reg_tutorials\code_data\data\landmark_data\T1GD_labels\cross4'
data_path_TOF_label = r'C:\Users\Administrator\Desktop\reg_tutorials\code_data\data\landmark_data\TOF_labels\cross4'
data_path_ddf = r'C:\Users\Administrator\Desktop\save\result_save\122'

a1 = 'case000002.nii.gz'
a2 = 'case000016.nii.gz'
a3 = 'case000018.nii.gz'
a4 = 'case000021.nii.gz'
a5 = 'case000022.nii.gz'
filename_T1GD_label0 = os.path.join(data_path_T1GD_label, a1)
filename_T1GD_label1 = os.path.join(data_path_T1GD_label, a2)
filename_T1GD_label2 = os.path.join(data_path_T1GD_label, a3)
filename_T1GD_label3 = os.path.join(data_path_T1GD_label, a4)
filename_T1GD_label4 = os.path.join(data_path_T1GD_label, a5)
filename_TOF_label0 = os.path.join(data_path_TOF_label, a1)
filename_TOF_label1 = os.path.join(data_path_TOF_label, a2)
filename_TOF_label2 = os.path.join(data_path_TOF_label, a3)
filename_TOF_label3 = os.path.join(data_path_TOF_label, a4)
filename_TOF_label4 = os.path.join(data_path_TOF_label, a5)
filename_ddf0 = os.path.join(data_path_ddf, 'ddf0.nii.gz')
filename_ddf1 = os.path.join(data_path_ddf, 'ddf1.nii.gz')
filename_ddf2 = os.path.join(data_path_ddf, 'ddf2.nii.gz')
filename_ddf3 = os.path.join(data_path_ddf, 'ddf3.nii.gz')
filename_ddf4 = os.path.join(data_path_ddf, 'ddf4.nii.gz')


def label_information(file_t1gd, file_tof):
    T1GD_label = nib.load(file_t1gd)
    TOF_label = nib.load(file_tof)
    T1GD_label_data = T1GD_label.get_data()
    TOF_label_data = TOF_label.get_data()
    # t1gd_data = np.expand_dims(np.expand_dims(np.asarray(np.flip(np.transpose(T1GD_label_data(0, 2, 1)), 2), dtype=np.float32), 0), -1)
    # tof_data = np.expand_dims(np.expand_dims(np.asarray(TOF_label_data,  dtype=np.float32), 0), -1)
    # t1gd_data = np.expand_dims(np.expand_dims(np.asarray(T1GD_label_data, dtype=np.float32), 0), -1)
    # tof_data = np.expand_dims(
    #     np.expand_dims(np.asarray(np.flip(np.transpose(TOF_label_data, (0, 2, 1)), 1), dtype=np.float32), 0), -1)
    t1gd_data = np.expand_dims(np.expand_dims(np.asarray(np.flip(np.transpose(T1GD_label_data, (0, 2, 1)), 2), dtype=np.float32),0), -1)
    tof_data = np.expand_dims(
        np.expand_dims(np.asarray(TOF_label_data, dtype=np.float32), 0), -1)
    return t1gd_data, tof_data


def load_ddf_data(ddf_path):
    ddf = nib.load(ddf_path)
    ddf_data = ddf.get_data()
    ddf_data = np.expand_dims(np.asarray(ddf_data, dtype=np.float32), 0)
    return ddf_data


def get_reference_grid(grid_size):
    return tf.cast(tf.stack(tf.meshgrid(
        [i for i in range(grid_size[0])],
        [j for j in range(grid_size[1])],
        [k for k in range(grid_size[2])],
        indexing='ij'), axis=3), dtype=tf.float32)


def compute_centroid_distance(input1, input2, grid=None):
    if grid is None:
        grid = get_reference_grid(input1.shape[0:3])

    def compute_centroid_1(mask, grid0):


        return tf.reduce_mean(tf.boolean_mask(grid0, mask >0), axis=0)


    c11 = compute_centroid_1(input1, grid)
    c21 = compute_centroid_1(input2, grid)

    return tf.sqrt(tf.reduce_sum(tf.square(c11 - c21), axis=0))

t1gd0_data, tof0_data = label_information(filename_T1GD_label0, filename_TOF_label0)
ddf0_data = load_ddf_data(filename_ddf0)
warped_label0 = apps.warp_volumes_by_ddf(tof0_data, ddf0_data)
warped_label0_data = np.squeeze(warped_label0)
t1gd0_data = np.squeeze(t1gd0_data)

t1gd1_data, tof1_data = label_information(filename_T1GD_label1, filename_TOF_label1)
ddf1_data = load_ddf_data(filename_ddf1)
warped_label1 = apps.warp_volumes_by_ddf(tof1_data, ddf1_data)
warped_label1_data = np.squeeze(warped_label1)
t1gd1_data = np.squeeze(t1gd1_data)

t1gd2_data, tof2_data = label_information(filename_T1GD_label2, filename_TOF_label2)
ddf2_data = load_ddf_data(filename_ddf2)
warped_label2 = apps.warp_volumes_by_ddf(tof2_data, ddf2_data)
warped_label2_data = np.squeeze(warped_label2)
t1gd2_data = np.squeeze(t1gd2_data)

t1gd3_data, tof3_data = label_information(filename_T1GD_label3, filename_TOF_label3)
ddf3_data = load_ddf_data(filename_ddf3)
warped_label3 = apps.warp_volumes_by_ddf(tof3_data, ddf3_data)
warped_label3_data = np.squeeze(warped_label3)
t1gd3_data = np.squeeze(t1gd3_data)

t1gd4_data, tof4_data = label_information(filename_T1GD_label4, filename_TOF_label4)
ddf4_data = load_ddf_data(filename_ddf4)
warped_label4 = apps.warp_volumes_by_ddf(tof4_data, ddf4_data)
warped_label4_data = np.squeeze(warped_label4)
t1gd4_data = np.squeeze(t1gd4_data)

spacing = 0.6

Lm_distance0 = compute_centroid_distance(t1gd0_data, warped_label0_data)

Lm_distance1 = compute_centroid_distance(t1gd1_data, warped_label1_data)

Lm_distance2 = compute_centroid_distance(t1gd2_data, warped_label2_data)

Lm_distance3 = compute_centroid_distance(t1gd3_data, warped_label3_data)

Lm_distance4 = compute_centroid_distance(t1gd4_data, warped_label4_data)
# tof0_data = np.squeeze(tof0_data)
# tof1_data = np.squeeze(tof1_data)
# tof2_data = np.squeeze(tof2_data)
# tof3_data = np.squeeze(tof3_data)
# tof4_data = np.squeeze(tof4_data)
# Lm_distance0 = compute_centroid_distance(t1gd0_data, tof0_data)
#
# Lm_distance1 = compute_centroid_distance(t1gd1_data, tof1_data)
#
# Lm_distance2 = compute_centroid_distance(t1gd2_data, tof2_data)
#
# Lm_distance3 = compute_centroid_distance(t1gd3_data, tof3_data)
#
# Lm_distance4 = compute_centroid_distance(t1gd4_data, tof4_data)

sess = tf.InteractiveSession()
Lm_distance0 = round(Lm_distance0.eval() * spacing, 3)
Lm_distance1 = round(Lm_distance1.eval() * spacing, 3)
Lm_distance2 = round(Lm_distance2.eval() * spacing, 3)
Lm_distance3 = round(Lm_distance3.eval() * spacing, 3)
Lm_distance4 = round(Lm_distance4.eval() * spacing, 3)
print("Lm_distance", Lm_distance0, Lm_distance1, Lm_distance2, Lm_distance3, Lm_distance4)
print("mean Lm_distance", round((Lm_distance0+Lm_distance1+Lm_distance2+Lm_distance3+Lm_distance4)/5, 3))