import rospy
from Simulation import AMBF
from Utlities import Read_Mocap
from Controller import PD_Controller
import numpy as np
from std_msgs.msg import Float64MultiArray
import time as clock
from lib.Python import RMP_runner
from Tkinter import *
import ambf_msgs.msg as ambf



def calculate_gain(Ku, Tu):
    Td = Tu / 8.0
    Kp = 0.8 * Ku
    Kd = (Ku * Tu) / 10.0
    return Kp, Kd


#
def go():


    # Kp = np.array(
    #     [0, sliders[0][0].get(), sliders[1][0].get(), sliders[2][0].get(), sliders[3][0].get(), sliders[4][0].get(),
    #      sliders[5][0].get()])
    #
    # Kd = np.array(
    #     [0, sliders[0][1].get(), sliders[1][1].get(), sliders[2][1].get(), sliders[3][1].get(), sliders[4][1].get(),
    #      sliders[5][1].get()])

    Controller.Kd = Kd
    Controller.Kp = Kp
    traj_h = Float64MultiArray()
    traj_k = Float64MultiArray()
    traj_a = Float64MultiArray()
    q = sim.q
    qd = sim.qd


    for ii in xrange(6):
        q_goal[ii] = 0
        qd_goal[ii] = 0
        qdd_goal[ii] = 0

    # q_goal[1] = -0.2
    # q_goal[4] = -0.2
    #
    # q_goal[2] = 0.2
    # q_goal[5] = 0.2

    aq = qdd_goal + Controller.calc(q_goal - q, qd_goal - qd)
    tau = sim.calculate_dynamics(q_d, qd_d, aq)

    for i in xrange(0, 6):
        cmd[i] = tau[i + 1]

    sim.send_command(cmd)

    traj_h.data.append(q_goal[1])
    traj_k.data.append(q_goal[2])
    traj_a.data.append(q_goal[3])
    traj_h.data.append(q_goal[4])
    traj_k.data.append(q_goal[5])
    traj_a.data.append(q_goal[6])

    traj_hip.publish(traj_h)
    traj_knee.publish(traj_k)
    traj_ankle.publish(traj_a)

    dt = sim.dt
    clock.sleep(0.01)
    #print dt*1000
    #root.after(10,go)


sim = AMBF.AMBF("revolute", 52, 1.57)
Lhip_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/hip_left.xml")
Lknee_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/knee_left.xml")
Lankle_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/ankle_left.xml")

Rhip_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/hip_right.xml")
Rknee_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/knee_right.xml")
Rankle_runner = RMP_runner.RMP_runner("/home/nathaniel/git/AMBF_Walker/config/ankle_right.xml")

traj_hip = rospy.Publisher("traj_hip", Float64MultiArray, queue_size=1)
traj_knee = rospy.Publisher("traj_knee", Float64MultiArray, queue_size=1)
traj_ankle = rospy.Publisher("traj_ankle", Float64MultiArray, queue_size=1)

q_d = np.asarray([0.0] * 7)
qd_d = np.asarray([0.0] * 7)
qdd_d = np.asarray([0.0] * 7)
q_goal = np.asarray([0.0] * 7)
qd_goal = np.asarray([0.0] * 7)
qdd_goal = np.asarray([0.0] * 7)
cmd = np.asarray([0.0] * 6)
dt = 0

#root = Tk()


gains = ( [ 510,36.8],[565,42.89],[354,45.2],[ 510,36.8],[565,42.89],[354,45.2])

Kp = np.array([0,gains[0][0],gains[1][0],gains[2][0],gains[3][0],gains[4][0],gains[5][0] ])
Kd = np.array([0,gains[0][1],gains[1][1],gains[2][1],gains[3][1],gains[4][1],gains[5][1] ])

Controller = PD_Controller.PDController(Kp, Kd)


if __name__ == "__main__":

    # cmd = ambf.ObjectCmd()
    # cmd.enable_position_controller = True
    # cmd.pose.orientation.w = 1
    # cmd.pose.position.z = 2.0
    #
    # sim.send_msg(cmd)
    # pose = np.linspace(2.5, 1.80, num=5)
    #
    # for h in pose:
    #     cmd.pose.position.z = h
    #     count = 0
    #     while count < .5:
    #         sim.send_msg(cmd)
    #         count += 0.01
    #         clock.sleep(0.01)
    #
    #
    # while 1:
    #     cmd.pose.position.z = 1.80
    #     sim.send_msg(cmd)

    cmd = ambf.ObjectCmd()
    cmd.enable_position_controller = False
    cmd.pose.orientation.w = 1
    cmd.wrench.force.z = 32.*9.81
    sim.send_msg(cmd)
    pose = np.linspace(2.5, 1.80, num=5)

    while 1:
        sim.send_msg(cmd)


#
# while 1:
#     cmd.pose.position.z = 1.80
#     sim.send_msg(cmd)










