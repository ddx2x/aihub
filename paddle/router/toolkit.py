from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile, Form
from typing import List, Optional
from pydantic import BaseModel, Field
from router.ai import groqAI
from router.ai import ai_ocr
from zhdate import ZhDate


router = APIRouter(tags=["默认路由"])


@router.post("/resume-parse")
async def resumeParse(pdf: Optional[UploadFile] = File(None), api_key: str = Form(None)):
    defaultPrompt = """你是一名专业和资深的超级HR和资深的面试官，请你帮我分析一下简历，需要给出一些结果给我，其中回答不能有多余的额外的回答，必须严格按照我下面的格式回答，规则如下：
	1. 整体评价: 满分100分，比如80分那就是 80/100 这种显示结果，而且需要包含大概的评价。
	2. 总结： 给出总结
	3. 缺点： 不少于10个，越多越好。
	4. 修改意见：以专业的HR知识，给出不下10点的专业修改意见，越多越好。
	5. 预估薪水：根据这份简历，从boss直聘上分析数据。根据当前国内就业环境，还有需要给出中国大陆一线城市，中国大陆二线城市。
	6. 面试的问题和答案： 请你分析他简历是属于什么职业，预测一些面试官可能提出的一些问题，并提供答案。
	回答格式如下：
	
	### 整体评价:
	  * xxx
	
	### 总结:
	  *  xxx
	
	### 缺点:
	  1. xxx
	  2. xxx
	
	### 修改意见:
	   1. xxx
	   2. xxx

	### 根据Boss直聘预估薪水:
	   1. xxx
	   2. xxx
	
	### 预测面试的问题和答案:
	   1. 问题：xxx
		  答案：xxx
	   2. 问题：xxx
		  答案：xxx
"""
    ocr_data = await ai_ocr(base64_imgs=None, pdf=pdf)
    if ocr_data["data"] == "":
        raise HTTPException(status_code=400, detail="ocr data is none")
    print(ocr_data["data"])
    messages = [
         {
            "role": "user",
            "content": "接下来我会问你一些问题，你只可以简体中文回答，绝对不可以出现其他语言",
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": defaultPrompt,
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": ocr_data["data"],
        },
    ]
    ai_answer = await groqAI(messages, "mixtral-8x7b-32768")
    return {"answer": ai_answer}


class fortuneRequest(BaseModel):
    baseInfo: Optional[str] = Field(None, description="")
    otherInfo: Optional[str] = Field(None, description="")


@router.post("/fortune")
async def fortune(request:fortuneRequest):
    defaultPrompt = """你是一名专业且资深的紫微斗数分析师，并且是在相关行业有多年的经验的资深从业者，我会发一个紫微命盘给你，请你帮我分析一下紫微命盘，需要给出一些结果给我，你需要围绕以下2个标题给我答案内容，规则如下：1.每个宫位的分析结果(此标题为一级目录)，二级目录为每个宫位的名称，然后三级目录为:天干、地支、主要星宿（需要显示亮度）、次要星宿、形容星宿，解析结果。2.总结整体运势(此标题为一级目录)，二级目录包括财富、爱情、事业，其中每个必须有3个分析作为三级目录。\n 以上内容必须遵从一级目录（前后各两个*），二级目录(4个空格后一个 )，三级目录(8个空格后一个)的规则，在直观上分为三层。以上在括号中的内容都是我给你的解释说明，不得复制。格式类似：** 每个宫位的分析结果 **\n * 子女宫\n * 天干。直接给我答案不需要你说别的
"""
    content = f'命盘基本信息：{request.baseInfo}\n  命盘宫位信息： {request.otherInfo}'
    print(content)
    messages = [
         {
            "role": "user",
            "content": "接下来我会问你一些问题，你只可以简体中文回答，绝对不可以出现其他语言，绝对不可以出现英文",
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": defaultPrompt,
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": content,
        },
    ]
    ai_answer = await groqAI(messages, "mixtral-8x7b-32768")
    return {"answer": ai_answer}


@router.post("/fortune-ym")
async def fortuneYM(request:fortuneRequest):
    defaultPrompt = """你是一名专业且资深的紫微斗数分析师，并且是在相关行业有多年的经验的资深从业者，我会发一个紫微命盘给你，请你帮我分析一下紫微命盘，需要给出一些结果给我，你需要围绕以下2个标题给我答案内容，规则如下：1.每个宫位的分析结果(此标题为一级目录)，二级目录为每个宫位的名称，然后三级目录为:天干、地支、主要星宿（需要显示亮度）、次要星宿、形容星宿，解析结果。2.总结整体运势(此标题为一级目录)，二级目录包括财富、爱情、事业，其中每个必须有3个分析作为三级目录。\n 以上内容必须遵从一级目录（前后各两个*），二级目录(4个空格后一个 )，三级目录(8个空格后一个)的规则，在直观上分为三层。以上在括号中的内容都是我给你的解释说明，不得复制。格式类似：** 每个宫位的分析结果 **\n * 子女宫\n * 天干。直接给我答案不需要你说别的
"""
    content = f'命盘基本信息：{request.baseInfo}\n  命盘宫位信息： {request.otherInfo}'
    print(content)
    messages = [
         {
            "role": "user",
            "content": "接下来我会问你一些问题，你只可以简体中文回答，绝对不可以出现其他语言,绝对不可以出现英文",
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": defaultPrompt,
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": content,
        },
    ]
    ai_answer = await groqAI(messages, "mixtral-8x7b-32768")

    zhday = ZhDate.today()
    content = f'''根据以上信息，今天是农历{zhday}，请帮我分析一下流年的运势，包整体流年运势，事业运势，财运运势，感情运势，健康运势，建议。
	格式如下：
	**总结整体运势**
		xxxxxx
	* 事业运势
		* xxxx
	* 财运运势
		* xxxx
    * 感情运势
		* xxxxx
	* 健康运势
		* xxxxx
	**建议**
		xxxxxx'''
    messages.append({ "role": "system", "content": ai_answer})
    messages.append({ "role": "user", "content": content})
    ai_answer = await groqAI(messages, "mixtral-8x7b-32768")
    return {"answer": ai_answer}


class contractRequest(BaseModel):
    type: Optional[str] = None
    pdf: Optional[UploadFile] = None
    other_info:Optional[str] = None


@router.post("/contract")
async def contract(request:contractRequest):

    ocr_data = await ai_ocr(base64_imgs=None, pdf=request.pdf)
    if ocr_data["data"] == "":
        raise HTTPException(status_code=400, detail="ocr data is none")
    print(ocr_data["data"])

    defaultPrompt = f'''我有一个关于合同的{request.type}需要咨询你，加下来我会发一份合同给你，需要你帮我修改，全部用简体中文回答，给我的回答包括：缺点(列出至少三个)、建议修改(列出至少三个)、其他建议(列出至少三个)
		你回答的格式如下:
		### 缺点：
		1. **xxx:** xxxx
		  
		2. **xxx:** xxxx
		
		3. **xxx:** xxxx
		
		### 建议修改：
		1. **xxx:** xxxx
		
		2. **xxx:** xxxx
		
		3. **xxx:** xxxx
		
		### 其他建议：
		1. **xxx:** xxxx
		
		2. **xxx:** xxxx
		
		3. **xxx:** xxxx
		'''

    if request.other_info == "" :
        request.other_info = "没有，你直接进行分析即可"

    messages = [
         {
            "role": "user",
            "content": "接下来我会问你一些问题，你只可以简体中文回答，绝对不可以出现其他语言,绝对不可以出现英文",
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": defaultPrompt,
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": f'合同内容如下:{ocr_data["data"]}',
        },
        {
            "role": "system",
            "content": "好的，你有什么要补充的吗",
        },
         {
            "role": "user",
            "content": request.other_info,
        },
    ]
    ai_answer = await groqAI(messages, "mixtral-8x7b-32768")

    return {"answer": ai_answer}
