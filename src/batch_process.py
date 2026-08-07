import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from llm_client import client


load_dotenv()


# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_BASE_URL")
# )



def analyze_text(text):

    response = client.chat.completions.create(

        model="gpt-5.5",

        messages=[
            {
                "role":"system",
                "content":
                """
                你是一个文本分析助手。
                返回JSON格式：
                {
                    "summary":"",
                    "keywords":[]
                }
                """
            },
            {
                "role":"user",
                "content":text
            }
        ],

        temperature=0
    )


    content = response.choices[0].message.content


    return json.loads(content)



def main():

    input_dir="input"
    output_dir="output"


    os.makedirs(output_dir,exist_ok=True)


    files=os.listdir(input_dir)


    success=0
    failed=0


    print("开始处理文件...")


    for index,file in enumerate(files,1):

        path=os.path.join(
            input_dir,
            file
        )


        print(
            f"\n[{index}/{len(files)}] 正在处理 {file}"
        )


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                text=f.read()


            result=analyze_text(text)


            output_file=os.path.join(
                output_dir,
                file.replace(
                    ".txt",
                    ".json"
                )
            )


            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    result,
                    f,
                    ensure_ascii=False,
                    indent=2
                )


            print("✓ 成功")

            success+=1


        except Exception as e:

            print(
                "✗ 失败:",
                e
            )

            failed+=1



    print("\n=================")
    print("处理完成")
    print("成功:",success)
    print("失败:",failed)
    print("=================")



if __name__=="__main__":
    main()
