import os
import yaml
import random
import json

from .llm import SingletonGPT

client = SingletonGPT.get_instance().gpt

with open("config/prompt.yaml") as stream:
    prompt = yaml.safe_load(stream)

with open("resource/hook.yaml") as stream:
    hook = yaml.safe_load(stream)

introduce_types = [
        "Đặt câu hỏi liên quan đến NỖI ĐAU CỦA NGƯỜI XEM, USP SẢN PHẨM, CÔNG DỤNG", 
        "Trả lời comment thắc mắc trong video của sản phẩm đối thủ",
        "Thu hút bằng giác quan: Thị giác, Thính giác, ASMR, làm các hành động LỐ tưởng như không ai làm được",
        "Sử dụng con số cụ thể: Mình đã chụp hết 1000 tấm ảnh của chiếc máy ảnh này",
        "Cụm từ tác động (Dừng ngay, Làm ngay điều này, đừng để...)",
        "Dùng người nổi tiếng (KOL)",
        "So sánh (So sánh sản phẩm với sản phẩm cùng công dụng hoặc sản phẩm đổi thủ)",
        "Kể câu chuyện cá nhân (Mình đã kiếm được 100M ở tuổi 20 như thế nào?)"
    ]

structures = [
    "Tập trung vào vấn đề, làm nổi bật cảm xúc, và đưa ra giải pháp.",
    "Dẫn dắt cảm xúc người xem từ tò mò đến hành động.",
    "So sánh trước và sau khi sử dụng sản phẩm.",
    "Nhấn mạnh vào tính năng, lợi ích và giá trị thực tế.",
    "Kể câu chuyện dẫn đến giải pháp.",
    "Thu hút bằng câu hỏi, cung cấp giải pháp, và làm nổi bật nhân vật chính.",
    "Dẫn dắt từ hiểu vấn đề đến hành động.",
    "Thiết kế để thu hút và khuyến khích mua ngay.",
    "Nâng cao nhận thức, giải thích, thuyết phục, và thúc đẩy hành động."
]

def generate_hook(structure, description, sample):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        n = 1,
        messages=[
            {
                "role": "user",
                "content": prompt["PROMPT_HOOK"].format(
                    structure,
                    description,
                    sample
                )
            }
        ]
    )

    return response.choices[0].message.content

def generate_introduce(introduce_type, structure, hook_sentence, description):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        n = 1,
        messages=[
            {
                "role": "user",
                "content": prompt["PROMPT_INTRO"].format(
                    introduce_type,
                    structure,
                    description,
                    hook_sentence
                )
            }
        ]
    )

    return response.choices[0].message.content

def generate_main(structure, description, hook_sentence, introduce):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        n = 1,
        messages=[
            {
                "role": "user",
                "content": prompt["PROMPT_MAIN"].format(
                    structure,
                    description,
                    hook_sentence,
                    introduce
                )
            }
        ]
    )

    return response.choices[0].message.content

def generate_end(structure, description, hook_sentence, introduce, main):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.8,
        n = 1,
        messages=[
            {
                "role": "user",
                "content": prompt["PROMPT_END"].format(
                    structure,
                    description,
                    hook_sentence,
                    introduce,
                    main
                )
            }
        ]
    )

    return response.choices[0].message.content


def genenrate_content(description):
    # genenrate hook
    structures_id = random.randint(0, len(structures) - 1)
    hook_sentence = generate_hook(
        structure=structures[structures_id],
        description=description,
        sample=hook["HOOK"])

    # generate introduce sentence
    intro_id = random.randint(0, len(introduce_types) - 1)
    introduce = generate_introduce(
        introduce_type=introduce_types[intro_id],
        structure=structures[structures_id],
        hook_sentence=hook_sentence,
        description=description
    )

    main = generate_main(
        structure=structures[structures_id],
        description=description,
        hook_sentence=hook_sentence,
        introduce=introduce
    )

    end = generate_end(
        structure=structures[structures_id],
        description=description,
        hook_sentence=hook_sentence,
        introduce=introduce,
        main=main
    )

    content = "Câu hook: " + hook_sentence + "\nPhần mở đầu: " + introduce + "\nPhần thân: " + main + "\nPhần cuối: " + end
    
    content = {
        "text": content
    }

    return json.dumps(content)