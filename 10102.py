from openai import OpenAI

client = OpenAI(
    api_key="sk-F4NlDHhzI2DDf0AvCMYagMYHPMExBJKuvFEVfP3hW7r56Bfi",
    base_url="https://api.moonshot.cn/v1",
)
messages1 = [
        {"role": "system",
         "content": "你是 Kimi"},
        {"role": "user", "content": "你好，接下来请你帮我处理一些代码"}
    ]

def chat(input: str=" "):
    messages1.append({
        "role": "user",
        "content": input,
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages1,
        temperature=0.3,
    )
    return completion.choices[0].message.content
def generate_new_prompt(content, pre_context, post_context):
    new_prompts = []
    for idx in range(len(content)):
      prompt = content[idx]['prompt'].replace('\n', '').replace('\r', '')
      pre_con = pre_context[idx]
      post_con = post_context[idx]
      front_context = "With the partial preceding codes provided as:"
      end_context = "and with the partial following codes provided as"
      new_promp = front_context + pre_con + ". " + prompt + " " + end_context + post_con
      new_promp = new_promp.replace(r' """ ', "")
      new_prompts.append(new_promp)
    combined_string = " ".join(new_prompts)
    return combined_string
    #return  new_prompts

def save_adv_snippet(new_prompt):
    messages1.append({ "role": "system", "content": "You are an experienced programmer." },
                )
    messages1.append({"role": "user", "content":new_prompt},)
    chat_output = chat()  # 调用 chat 函数，但不需要立即返回
    return chat_output

def main():
    content = [{"prompt": "请在函数中添加一些无功能影响的代码行，以隐蔽方式修改该函数。"}]
    pre_context = ["int add(int a, int b) {"]
    post_context = [" return a + b; }"]
    print(messages1)
    adv_snippet = save_adv_snippet(generate_new_prompt(content, pre_context, post_context))
    print(chat())
    print("生成的对抗样本：\n", adv_snippet)
    #print("更新后的消息：\n", messages1)

if __name__ == "__main__":
    main()