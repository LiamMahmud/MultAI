# TEXT WHEN YOU HOVER OVER TEXT
'''
    st.sidebar.markdown("""
        <style>
            .tooltip {
                position: relative;
                display: inline-block;
                border-bottom: 1px dotted black;
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                width: 120px;
                background-color: black;
                color: white;
                text-align: center;
                border-radius: 6px;
                padding: 5px 0;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -60px;
                opacity: 0;
                transition: opacity 0.3s;
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div class="tooltip">
            Temperature
            <span class="tooltiptext">Adjust the temperature parameter</span>
        </div>: <br>
        <div class="tooltip">
            Top P
            <span class="tooltiptext">Adjust the top P parameter</span>
        </div>: <br>
        <div class="tooltip">
            Max Length
            <span class="tooltiptext">Adjust the maximum length parameter</span>
        </div>: <br>
    """, unsafe_allow_html=True)
'''