import gradio as gr
import json

from send_post import do_post

body = {
    "style": "",
    "content": ""
}
def_text = """
The long history of the Israeli-Palestinian conflict is filled with bloodshed, dislocation and trauma. But even by those relative standards, the current conflagration stands out. For one thing, it’s especially brutal. Not since the Holocaust have as many Jews been massacred at one time as were on Oct. 7, when Hamas militants stormed Israel, killing 1,400 people and taking more than 200 hostage. Before Israel escalated its ground operations in the Hamas-run Gaza Strip, its retaliatory strikes, mostly from the air, killed more than 7,700, according to Gazan authorities, and dislocated nearly half the population of 2.3 million, by an estimate of UN officials. Israel’s decision to cut off power to Gaza — and severely limit water and food supplies — threatens a larger humanitarian calamity.

Beyond that, this new chapter has changed the way Israelis see the threat from the Islamist group, and thus the measures they’re prepared to take against it. From the start, Hamas, which the US and European Union designate a terrorist organization, has been dedicated to the destruction of the state of Israel. For three decades, it’s held to that mission as other Palestinian leaders have committed to peaceful coexistence with Israel while pursuing their own state alongside it. Hamas considers all of the Holy Land — which encompasses what today is Israel, the West Bank and Gaza — a divine Islamic endowment, and pledges in its charter to destroy Israel by any means. After Hamas showed what it’s capable of on Oct. 7, Israelis now say they are determined not just to suppress the group but to dismantle it, a goal that will entail more bloodshed and may not be achievable.

How We Got Here
The modern struggle between Arabs and Jews over ownership of the Holy Land is rooted in the nationalism that grew among both groups after the World War I-era collapse of the Ottoman Empire, which had ruled the territory for centuries. In 1920, the war’s victors gave the UK a mandate to administer what was then called Palestine. Intercommunal fighting in the territory was exacerbated by resistance among Arabs to Jewish immigration, which rose in the 1930s; in the face of Nazi persecution, increasing numbers of Jews from abroad sought sanctuary in their ancient homeland, where Jews have lived for nearly 4,000 years.

Read More: Understanding the Roots of the Israel-Hamas War

In an effort to stop Arab-Jewish violence, a British commission in 1937 proposed partitioning the territory to create a state for each group. A decade later, the United Nations endorsed a different division. The Arabs said no both times, while the Jews said yes. After declaring its independence in 1948, Israel was attacked by neighboring Arab states, and its wartime gains established the borders of the new nation. The Palestinians use the term Nakba, or disaster, to refer to this period, which produced an estimated 700,000 Palestinian refugees. Many of them fled to the Gaza Strip, then under Egyptian control.
"""

def update(format, content ):
    # return f"Welcome to Gradio, {format} {content}!"
    # bdy = content.replace("\n\n","")
    bdy = content.replace("\n\n","")
    bdy = bdy.replace("\r\n","")
    bdy = bdy.replace("\n", "")
    # res = do_post("/api/v1/summarize/", {"style": format, "content":bdy })) 
    print({"style": format, "content":bdy })
    print("\n-----------------------")
    res = do_post("/aipex/summarize",{"style": format, "content":bdy })
    
    print(str(res.status_code) + " | " + res.text)
 
    return json.loads(res.text)["summary"]

 
with gr.Blocks() as demo:
    gr.Markdown("## Text Summary Demo.")
    gr.Image("https://python.langchain.com/assets/images/map_reduce-c65525a871b62f5cacef431625c4d133.jpg")
    format = gr.Radio(["one_sentence", "bullet_points", "short", "long"],value="one_sentence",  label="스타일", info="Select a Summary Style")
    with gr.Row():
        with gr.Column():
            
            inp = gr.TextArea(lines=10, value=def_text, autoscroll=True, label="요약할 문장", placeholder="요약할 문장을 입력하세요")
        with gr.Column():
            out = gr.TextArea(lines=16, autoscroll=True, label="요약문", placeholder="요약  메세지 ")
    btn = gr.Button("Run")
    
   
    btn.click(fn=update, inputs=[format, inp], outputs=out)

demo.launch(share=False, server_port=8000)
