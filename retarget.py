import os
import bpy

pelvis = ['pelvis', 'hips']
spine = ['spine', 'chest']
arm = ['arm','upperarm']
forearm = ['forearm','lowerarm']
thigh = ['thigh', 'upleg']
calf = ['calf', 'leg']
foot = ['foot']
hand = ['hand']
neck = ['neck']
head = ['head']
clavicle = ['shoulder', 'clavicle']
left = ['left', '_l', ',l']
right = ['right', '_r', ',r']
BONE_NAMES = pelvis + spine + arm + forearm + thigh + calf + foot + hand + neck + head + clavicle 

skeletons = []

class SkeletonData:
    objname = ''
    keyframes = 0
    boneNames = []
    
skeletonDatas = []

def findBoneName(bname, targetBoneNameList):
    
    uselist = None
    isleft = False
    isright = False
    Collection = [pelvis,spine,arm,forearm,thigh,calf,foot , hand, neck, head,clavicle ]
    
    for i in Collection:
        for bn in i:  
            if bn in bname.lower():
                uselist = i
                break
                
    for bn in left:
        if bn in bname.lower():
           isleft = True
             
    for bn in right:
        if bn in bname.lower():
            isright = True          
                                   
    for x in uselist:
        for y in targetBoneNameList:
            if x in y.lower():
                if isleft:
                    for bn in left:
                        if bn in y.lower():
                            return y     
                elif isright:
                    for bn in right:
                        if bn in y.lower():
                            return y        
                else:
                    return y       
    return i[0]

# get selected skeletons and add them to list
for i in bpy.context.selected_objects:
    if i.type == "ARMATURE" :
        skeletons.append(i)
    
# create skelton data
for x in skeletons:
    
    #Select Skeleton
    x.select_set(True)
    bpy.context.view_layer.objects.active = x
      
    numKeyFrames = 0
    #check animation keyframes
    if x.animation_data is not None and x.animation_data.action is not None:
        for fc in x.animation_data.action.fcurves:       
            if len(fc.keyframe_points) > 0 :
                numKeyFrames = len(fc.keyframe_points)
                break

    # bone names
    bones = []
    for i in bpy.context.object.pose.bones:
        bones.append(i.name)
        
    data = SkeletonData()
    data.objname = x.name
    data.boneNames = bones
    data.keyframes = numKeyFrames
    skeletonDatas.append(data)
    
# sort by keyframe length
skeletonDatas.sort(key=lambda x:x.keyframes)

if len(skeletonDatas) > 1 :
    
    userSkeleton = bpy.data.objects[skeletonDatas[0].objname]
    targetSkeleton = bpy.data.objects[skeletonDatas[1].objname]
    
    #Select Skeleton
    userSkeleton.select_set(True)
    bpy.context.view_layer.objects.active = userSkeleton
    bpy.ops.object.posemode_toggle()

    for b in skeletonDatas[0].boneNames:     
        hasName = False
        for bn in BONE_NAMES:
            if bn in b.lower():
                hasName = True
        if hasName:
            constraint = bpy.context.object.pose.bones[b].constraints.new('COPY_ROTATION')
            constraint.target  = targetSkeleton
            constraint.subtarget = findBoneName(b, skeletonDatas[1].boneNames)

        
