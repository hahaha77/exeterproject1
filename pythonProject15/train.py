from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_curve, auc
from tqdm import tqdm
from data_process import *
from DQN import *
from env import *

if __name__ == "__main__":
    episodes = 100
    batch_size = 64
    state_data, x_test, action_data, y_test = data_process()

    print("State shape:", state_data.shape)
    print("Action shape:", action_data.shape)
    state_size = state_data.shape[1]
    action_size = action_data.shape[1]
    agent = DQNAgent(state_size, action_size)
    env = BreastCancerEnv(state_data, action_data)
    for e in tqdm(range(episodes), desc="Training Episodes"):
        state = env.reset()
        total_reward = 0
        while True:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            if done:
                print(f"episode: {e + 1}/{episodes}, score: {total_reward}, e: {agent.epsilon:.2}")
                agent.save(f"breast-cancer-dqn-{e+1}.pth")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)


    new_env = BreastCancerEnv(x_test, y_test)
    state = new_env.reset()
    state = np.array(state)
    total_reward = 0
    actions = []

    for time in range(len(new_env.state_data)):
        action = agent.act(state)
        next_state, reward, done, _ = new_env.step(action)
        next_state = np.array(next_state)

        total_reward += reward
        actions.append(list(action))
        state = next_state

        if done:
            break
    print(f"Total reward: {total_reward}")
    actions = np.array(actions)
    for i in range(3):
        print(f"Class {i+1} metrics:")
        accuracy = accuracy_score(y_test.to_numpy()[:, i], actions[:, i])
        recall = recall_score(y_test.to_numpy()[:, i], actions[:, i])
        precision = precision_score(y_test.to_numpy()[:, i], actions[:, i])
        f1 = f1_score(y_test.to_numpy()[:, i], actions[:, i])
        print(f"  Accuracy: {accuracy}")
        print(f"  Recall: {recall}")
        print(f"  Precision: {precision}")
        print(f"  F1 Score: {f1}")

    # 计算总体的指标
    overall_accuracy = accuracy_score(y_test.to_numpy().flatten(), actions.flatten())
    overall_recall = recall_score(y_test.to_numpy().flatten(), actions.flatten(), average='macro')
    overall_precision = precision_score(y_test.to_numpy().flatten(), actions.flatten(), average='macro')
    overall_f1 = f1_score(y_test.to_numpy().flatten(), actions.flatten(), average='macro')

    print("Overall metrics:")
    print(f"  Accuracy: {overall_accuracy}")
    print(f"  Recall: {overall_recall}")
    print(f"  Precision: {overall_precision}")
    print(f"  F1 Score: {overall_f1}")

    fpr, tpr, _ = roc_curve(y_test.to_numpy().flatten(), actions.flatten())
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()
