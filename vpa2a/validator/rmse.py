import bvhio
import numpy as np

# define the joint mapping

# edge to library mapping
edge_library_joint_map = [
    ("Pelvis", "hips_JNT"),
    ("Left_hip", "l_upleg_JNT"),
    ("Left_knee", "l_leg_JNT"),
    ("Left_ankle", "l_foot_JNT"),
    ("Left_foot", "l_toebase_JNT"),
    ("Right_hip", "r_upleg_JNT"),
    ("Right_knee", "r_leg_JNT"),
    ("Right_ankle", "r_foot_JNT"),
    ("Right_foot", "r_toebase_JNT"),
    ("Spine1", "spine_JNT"),
    ("Spine2", "spine1_JNT"),
    ("Spine3", "spine2_JNT"),
    ("Neck", "neck_JNT"),
    ("Head", "head_JNT"),
    ("Left_shoulder", "l_shoulder_JNT"),
    ("Left_elbow", "l_arm_JNT"),
    ("Left_wrist", "l_forearm_JNT"),
    ("Left_palm", "l_hand_JNT"),
    ("Right_shoulder", "r_shoulder_JNT"),
    ("Right_elbow", "r_arm_JNT"),
    ("Right_wrist", "r_forearm_JNT"),
    ("Right_palm", "r_hand_JNT")
]

# edge to edge mapping
edge_edge_joint_map = [
    ('Pelvis', 'Pelvis'),
    ('Left_hip', 'Left_hip'),
    ('Left_knee', 'Left_knee'),
    ('Left_ankle', 'Left_ankle'),
    ('Left_foot', 'Left_foot'),
    ('Right_hip', 'Right_hip'),
    ('Right_knee', 'Right_knee'),
    ('Right_ankle', 'Right_ankle'),
    ('Right_foot', 'Right_foot'),
    ('Spine1', 'Spine1'),
    ('Spine2', 'Spine2'),
    ('Spine3', 'Spine3'),
    ('Neck', 'Neck'),
    ('Head', 'Head'),
    ('Left_shoulder', 'Left_shoulder'),
    ('Left_elbow', 'Left_elbow'),
    ('Left_wrist', 'Left_wrist'),
    ('Left_palm', 'Left_palm'),
    ('Right_shoulder', 'Right_shoulder'),
    ('Right_elbow', 'Right_elbow'),
    ('Right_wrist', 'Right_wrist'),
    ('Right_palm', 'Right_palm')
]

# library to library mapping
library_library_joint_map = [
    ("hips_JNT", "hips_JNT"),
    ("l_upleg_JNT", "l_upleg_JNT"),
    ("l_leg_JNT", "l_leg_JNT"),
    ("l_foot_JNT", "l_foot_JNT"),
    ("l_toebase_JNT", "l_toebase_JNT"),
    ("r_upleg_JNT", "r_upleg_JNT"),
    ("r_leg_JNT", "r_leg_JNT"),
    ("r_foot_JNT", "r_foot_JNT"),
    ("r_toebase_JNT", "r_toebase_JNT"),
    ("spine_JNT", "spine_JNT"),
    ("spine1_JNT", "spine1_JNT"),
    ("spine2_JNT", "spine2_JNT"),
    ("neck_JNT", "neck_JNT"),
    ("head_JNT", "head_JNT"),
    ("l_shoulder_JNT", "l_shoulder_JNT"),
    ("l_arm_JNT", "l_arm_JNT"),
    ("l_forearm_JNT", "l_forearm_JNT"),
    ("l_hand_JNT", "l_hand_JNT"),
    ("r_shoulder_JNT", "r_shoulder_JNT"),
    ("r_arm_JNT", "r_arm_JNT"),
    ("r_forearm_JNT", "r_forearm_JNT"),
    ("r_hand_JNT", "r_hand_JNT")
]

def transform_edge_bvh(bvh):
    '''
    Specific transformation to re-align the EDGE BVH output to match library BVH output
    '''
    bvh.RestPose.Scale = 1
    bvh.RestPose.addEuler((-90, 0, 0))
    bvh.RestPose.PositionWorld = (-40,-95,40)
    bvhio.writeHierarchy('edge-transformed.bvh', bvh, 1/30)
    return bvh

def compute_rmse(edge_bvh_fp, lib_bvh_fp, joint_map=edge_library_joint_map):
    '''
    Read BVH file from edge output and library, compute the Root Mean Square Error
    Normalize the value to frame count
    
    '''
    root1 = bvhio.readAsHierarchy(edge_bvh_fp)
    root2 = bvhio.readAsHierarchy(lib_bvh_fp)

    # to find the min frame count to assess if both have different total frame count
    min_frame_count = min(bvhio.readAsBvh(edge_bvh_fp).FrameCount, bvhio.readAsBvh(lib_bvh_fp).FrameCount)

    results = {}
    deep_pos = 0
    edge_pos = 0
    for joint_name in joint_map:
        rms_total = 0
        for i in range(min_frame_count):  # Iterating from 0 to the min frame between to BVH
            pose_number = i
            pose_data1 = root1.loadPose(pose_number).layout()
            
            # Loop through the pose data to find the joint_name
            for joint, index, depth in pose_data1:
                if joint.Name == joint_name[0]:
                    edge_pos = joint.PositionWorld

            pose_data2 = root2.loadPose(pose_number).layout()

            for joint, index, depth in pose_data2:
                if joint.Name == joint_name[1]:
                    deep_pos = joint.PositionWorld
                    #print(deep_pos)

            diff_pos = edge_pos - deep_pos
            # Calculate RMS
            rms = np.sqrt(np.mean(diff_pos**2))
            # print("RMS of the vector:", rms)

            rms_total = rms_total + rms


        # Storing the result with the first item of the tuple as the key
        # dividing the rms total against frame count to make rmse independent of frame count
        results[joint_name[0]] = rms_total/min_frame_count
    return sum(results.values())

