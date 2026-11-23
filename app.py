import os
import io
import re
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Hoa Phượng AI Assistant', page_icon='🌸', layout='wide')
st.title('🌸 HOA PHƯỢNG AI ASSISTANT')
st.caption('PGD Hoa Phượng – VietinBank Chi nhánh Lê Chân | Bản demo sử dụng dữ liệu giả lập')
st.warning('Không nhập dữ liệu khách hàng thật, thông tin bí mật hoặc tài liệu nội bộ chưa được phép. Chức năng AI chỉ hoạt động khi đã cấu hình API được phê duyệt.')

if 'tasks' not in st.session_state:
    st.session_state.tasks = [{'Tên việc':'Chuẩn bị bài dự thi','Người phụ trách':'Đội thi','Hạn':str(date(2026,11,29)),'Trạng thái':'Đang thực hiện'}]

with st.sidebar:
    st.header('Cấu hình')
    model = st.text_input('Tên mô hình AI', value='gpt-4o-mini')
    api_key = st.text_input('API key (chỉ dùng khi được phép)', type='password', value=os.getenv('OPENAI_API_KEY',''))
    st.caption('Không có API: các chức năng dữ liệu, mẫu văn bản và quản lý việc vẫn chạy; chatbot hiển thị tình huống mẫu, không giả làm AI.')

home, chat, docs, draft, report, tasks = st.tabs(['🏠 Tổng quan','🤖 Trợ lý AI','📚 Tra cứu tài liệu','📝 Soạn văn bản','📊 Báo cáo Excel','📋 Công việc'])

def call_ai(prompt):
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        res = client.chat.completions.create(model=model, messages=[{'role':'system','content':'Bạn là trợ lý soạn thảo và phân tích cho một bản demo ngân hàng sử dụng dữ liệu giả lập. Không bịa quy định nội bộ, không đưa ra quyết định tín dụng, không khẳng định thông tin chưa có nguồn.'},{'role':'user','content':prompt}], temperature=0.2)
        return res.choices[0].message.content
    except Exception as exc:
        st.error(f'Không thể kết nối AI: {type(exc).__name__}. Kiểm tra cấu hình, quyền truy cập và kết nối mạng.')
        return None

with home:
    st.subheader('Một nơi hỗ trợ nhiều tác vụ thường ngày')
    c1,c2,c3 = st.columns(3)
    c1.metric('Nhóm chức năng', '5')
    c2.metric('Công việc đang theo dõi', len(st.session_state.tasks))
    c3.metric('Chế độ', 'AI thực' if api_key else 'Demo không API')
    st.info('Kịch bản trình diễn: tải bảng số liệu giả lập → xem biểu đồ → tạo bản nhận xét → soạn email → quản lý công việc. Chức năng trả lời AI linh hoạt cần API.')

with chat:
    st.subheader('Trợ lý hỏi đáp')
    question = st.text_area('Nhập câu hỏi', placeholder='Ví dụ: Hãy đề xuất cấu trúc báo cáo kết quả hoạt động tuần của phòng giao dịch')
    if st.button('Gửi câu hỏi', key='ask'):
        if not question.strip(): st.warning('Hãy nhập câu hỏi.')
        elif api_key:
            answer = call_ai(question)
            if answer: st.write(answer)
        else:
            st.info('CHẾ ĐỘ MÔ PHỎNG – chưa kết nối mô hình AI.')
            st.write('Gợi ý cấu trúc báo cáo tuần: (1) Kết quả chính; (2) So sánh kế hoạch; (3) Công việc tồn đọng; (4) Rủi ro cần lưu ý; (5) Kiến nghị tuần tới. Đây là nội dung mẫu cố định, không phải câu trả lời do AI tạo.')

with docs:
    st.subheader('Tìm kiếm trong tài liệu demo')
    up = st.file_uploader('Tải tài liệu TXT hoặc PDF không nhạy cảm', type=['txt','pdf'], key='doc')
    content = ''
    if up:
        if up.name.lower().endswith('.txt'):
            content = up.getvalue().decode('utf-8',errors='replace')
        else:
            try:
                from pypdf import PdfReader
                reader=PdfReader(io.BytesIO(up.getvalue()))
                content='\n'.join(p.extract_text() or '' for p in reader.pages)
            except Exception:
                st.error('Không đọc được PDF. Hãy dùng PDF có lớp văn bản hoặc TXT.')
    else:
        content = 'TÀI LIỆU GIẢ LẬP\nQuy trình tiếp nhận yêu cầu: ghi nhận yêu cầu, kiểm tra thông tin theo quy định được phê duyệt, chuyển cán bộ phụ trách, theo dõi kết quả.\nQuy trình báo cáo: tổng hợp dữ liệu, kiểm tra số liệu, trình người phụ trách phê duyệt.'
    query=st.text_input('Từ khóa tra cứu', key='query')
    if query:
        lines=[x.strip() for x in re.split(r'[\n.!?]+',content) if x.strip()]
        tokens=[t.lower() for t in re.findall(r'\w+',query) if len(t)>2]
        hits=[(sum(t in line.lower() for t in tokens),line) for line in lines]
        hits=sorted([x for x in hits if x[0]>0],reverse=True)[:5]
        if hits:
            st.caption('Kết quả khớp từ khóa, không phải câu trả lời AI và không xác minh hiệu lực quy định.')
            for _,line in hits: st.write('• '+line)
        else: st.info('Không tìm thấy đoạn phù hợp.')
    if api_key and st.button('Tóm tắt tài liệu bằng AI'):
        answer=call_ai('Chỉ tóm tắt nội dung được cung cấp, nêu rõ giới hạn nguồn:\n'+content[:16000])
        if answer: st.write(answer)

with draft:
    st.subheader('Soạn văn bản theo mẫu')
    kind=st.selectbox('Loại văn bản',['Email nhắc tiến độ','Thông báo họp','Báo cáo công việc'])
    receiver=st.text_input('Người nhận / đơn vị (giả lập)',value='Các thành viên đội thi')
    subject=st.text_input('Chủ đề',value='Tiến độ chuẩn bị sản phẩm demo')
    details=st.text_area('Nội dung chính',value='Hoàn thiện kiểm thử sản phẩm và rà soát tài liệu trước hạn nộp.')
    if st.button('Tạo bản nháp'):
        if api_key:
            out=call_ai(f'Soạn {kind} tiếng Việt chuyên nghiệp, chỉ dùng thông tin sau: người nhận {receiver}; chủ đề {subject}; nội dung {details}. Không bịa thông tin.')
        else:
            out=f'Kính gửi {receiver},\n\nVề việc: {subject}.\n\n{details}\n\nĐề nghị các bên liên quan phối hợp thực hiện và phản hồi tiến độ.\n\nTrân trọng.'
            st.caption('Bản nháp theo mẫu cố định, chưa dùng AI.')
        if out:
            st.text_area('Bản nháp – cần kiểm tra trước khi sử dụng',out,height=230)
            st.download_button('Tải bản nháp TXT',out.encode('utf-8'),'ban_nhap.txt','text/plain')

with report:
    st.subheader('Phân tích số liệu Excel/CSV giả lập')
    st.caption('Chỉ tải dữ liệu giả lập hoặc dữ liệu được phép xử lý trên nền tảng này.')
    f=st.file_uploader('Tải XLSX hoặc CSV',type=['xlsx','csv'],key='sheet')
    if f:
        try:
            df=pd.read_csv(f) if f.name.lower().endswith('.csv') else pd.read_excel(f)
        except Exception as exc:
            st.error('Không đọc được tệp. Kiểm tra định dạng.'); df=None
    else:
        df=pd.DataFrame({'Tháng':['T1','T2','T3','T4','T5','T6'],'Số lượt phục vụ':[120,138,141,155,149,171],'Yêu cầu hoàn tất':[111,130,132,149,140,165]})
        st.info('Đang hiển thị dữ liệu mẫu giả lập.')
    if df is not None:
        st.dataframe(df, use_container_width=True)
        numeric=df.select_dtypes(include='number').columns.tolist()
        if numeric:
            col=st.selectbox('Chỉ tiêu biểu đồ',numeric)
            labels=df.columns[0]
            st.bar_chart(df.set_index(labels)[col])
            st.write(f'Tổng {col}: **{df[col].sum():,.0f}** | Trung bình: **{df[col].mean():,.1f}**')
            summary=f'Báo cáo dữ liệu giả lập\nSố dòng: {len(df)}\nChỉ tiêu: {col}\nTổng: {df[col].sum():,.0f}\nTrung bình: {df[col].mean():,.1f}\n'
            if api_key and st.button('Nhận xét bằng AI'):
                ans=call_ai('Nhận xét ngắn gọn dữ liệu sau, không suy diễn ngoài bảng:\n'+df.head(30).to_csv(index=False))
                if ans: st.write(ans)
            st.download_button('Tải báo cáo TXT',summary.encode('utf-8'),'bao_cao_demo.txt','text/plain')
        else: st.warning('Không tìm thấy cột số để lập biểu đồ.')

with tasks:
    st.subheader('Theo dõi công việc – lưu tạm trong phiên truy cập')
    with st.form('newtask'):
        name=st.text_input('Tên công việc')
        owner=st.text_input('Người phụ trách')
        deadline=st.date_input('Hạn hoàn thành',value=date(2026,11,29))
        status=st.selectbox('Trạng thái',['Chưa bắt đầu','Đang thực hiện','Hoàn thành'])
        submitted=st.form_submit_button('Thêm công việc')
        if submitted:
            if name.strip():
                st.session_state.tasks.append({'Tên việc':name,'Người phụ trách':owner,'Hạn':str(deadline),'Trạng thái':status})
                st.success('Đã thêm công việc vào phiên hiện tại.')
            else: st.warning('Nhập tên công việc.')
    task_df=pd.DataFrame(st.session_state.tasks)
    st.dataframe(task_df,use_container_width=True)
    st.download_button('Xuất danh sách CSV',task_df.to_csv(index=False).encode('utf-8-sig'),'cong_viec_demo.csv','text/csv')
    st.caption('Dữ liệu công việc chưa được lưu vào cơ sở dữ liệu; tải CSV để lưu lại.')

st.divider()
st.caption('Bản thử nghiệm phục vụ cuộc thi. Không phải sản phẩm chính thức của VietinBank; nội dung AI cần người có thẩm quyền kiểm tra trước khi sử dụng.')
