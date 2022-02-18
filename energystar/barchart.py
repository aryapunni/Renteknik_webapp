#!/usr/bin/env python3
import matplotlib.pyplot as plt


# labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# values = [452, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# width = 0.25

# f, (ax1, ax2, ax3, ax4) = plt.subplots(2, 2, sharey=True)
# ax1.plot(labels, values)
# ax1.set_title('Sharing Y axis')
# ax2.scatter(labels, values)

# plt.subplots(2, 2, sharey='row')
# plt.show()
def example_plot(ax, labels, values):

    # ax.set_xticklabels(labels, fontsize=5)
    # plt.bar(x_pos, height, color=['black', 'red', 'green', 'blue', 'cyan'])
    ax.tick_params(axis='x', labelsize=5, color='red', labelcolor='red')
    ax.bar(labels, values, color='blue', width=0.5)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_xlabel('energy', fontsize=12, color='blue')
    ax.set_ylabel('y-label', fontsize=12)
    ax.set_title('Title', fontsize=14)


if __name__ == "__main__":
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [452, 300, 200, 450, 400, 0, 0, 0, 0, 0, 0, 0]
    fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True)

    for ax in axs.flat:
        for value in values:
            example_plot(ax, labels, value)


    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    fig.suptitle('Sharing x per column, y per row')
    ax1.plot(labels, values)
    ax2.plot(labels, values, 'tab:orange')
    ax3.plot(labels, values, 'tab:green')
    ax4.plot(labels, values, 'tab:red')

    for ax in fig.get_axes():
        ax.label_outer()


####################################################################
#############################Seaborn################################
####################################################################


    plt.show()
