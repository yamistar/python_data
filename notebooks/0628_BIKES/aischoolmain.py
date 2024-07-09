import streamlit as st
import finance_naver_copy   ##### finance_naver_copy.py 임포트
import bikes_da             ##### bikes_da.py 임포트
import meteor_shower_copy   ##### meteor_shower_copy.py 임포트

# 사이드바
st.sidebar.header('로그인')
user_id = st.sidebar.text_input("아이디 입력", value='streamlit', max_chars=15)
user_password = st.sidebar.text_input("패스워드 입력", value="1234", type='password')

if user_password == '1234':
    st.sidebar.header("파이썬 기초")
    opt_data =['','환율조회','따릉이','유성우']
    menu = st.sidebar.selectbox("메뉴 선택", opt_data, index=0)
    st.sidebar.write('선택한 메뉴 : ', menu)

    if menu == "환율조회" :
        st.subheader("환율조회>>>>>>>")
        finance_naver_copy.exchange_main() ###### finance_naver_copy.py의 exchange_main()호출

    elif menu == "따릉이" :
        st.subheader("따릉이 데이터 분석>>>>>>>>")
        bikes_da.bikes_da()

    elif menu == "유성우" :
        st.subheader("유성우 데이터 분석>>>>>>>>")
        meteor_shower_copy.shower_viewing_main()

    else :
        st.subheader("환영합니다.")

# 메인화면
# st.subheader("환영합니다")

# pip list --format=freeze > requirements.txt
