import streamlit as st
from streamlit_extras.chart_container import chart_container
from pandas import Timestamp as PandasTimestamp

class PatientVitalSigns:
    def __init__(self, vital_signs):
        self.vital_signs = vital_signs
    
    @st.fragment
    def render(self):
        st.header("Signos Vitales")

        # Add date range filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Fecha inicial",
                min_value=self.vital_signs['Fecha'].min(),
                max_value=self.vital_signs['Fecha'].max(),
                value=self.vital_signs['Fecha'].min(),
                key="start_date"  # Unique key for the widget
            )
        with col2:
            end_date = st.date_input(
                "Fecha final", 
                min_value=self.vital_signs['Fecha'].min(),
                max_value=self.vital_signs['Fecha'].max(),
                value=self.vital_signs['Fecha'].max(),
                key="end_date"  # Unique key for the widget
            )

        # Use session state to store filtered data
        if "filtered_data" not in st.session_state:
            st.session_state.filtered_data = self.vital_signs[
                (self.vital_signs['Fecha'] >= PandasTimestamp(start_date)) & 
                (self.vital_signs['Fecha'] <= PandasTimestamp(end_date))
            ]

        # Update filtered data only if the date range changes
        if (
            st.session_state.get("prev_start_date") != start_date or
            st.session_state.get("prev_end_date") != end_date
        ):
            st.session_state.filtered_data = self.vital_signs[
                (self.vital_signs['Fecha'] >= PandasTimestamp(start_date)) & 
                (self.vital_signs['Fecha'] <= PandasTimestamp(end_date))
            ]
            st.session_state.prev_start_date = start_date
            st.session_state.prev_end_date = end_date

        filtered_data = st.session_state.filtered_data

        st.markdown("""
            <style>
            .flex-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
            }
            .flex-item {
                flex: 1 1 45%;
                margin: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="flex-container">', unsafe_allow_html=True)

            vital_signs_labels = list(filtered_data.keys()[1:])
            vital_signs_measurements = ("°C", "total", "%", "total", "total", "%")
            container_tabs = ("Grafica 📈", "Datos 📄", "Exportar 📁")
            colors = ["#FF5733", "#33FF57", "#5733FF", "#FF33D1", "#33D1FF", "#D1FF33"]

            
            for i, sign_label in enumerate(vital_signs_labels):
                st.markdown('<div class="flex-item">', unsafe_allow_html=True)
                with chart_container(filtered_data, container_tabs):
                    sign_mean = filtered_data[sign_label].mean()
                    sign_max = filtered_data[sign_label].max()
                    sign_min = filtered_data[sign_label].min()
                    sign_measurement = vital_signs_measurements[i]

                    st.markdown(f"<h3 style='text-align: center;'>{sign_label}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='text-align: center;'> Máximo: {sign_max:.2f} {sign_measurement}    -   Mínimo: {sign_min:.2f} {sign_measurement}   -   Promedio: {sign_mean:.2f} {sign_measurement}</h4>", unsafe_allow_html=True)

                    st.line_chart(
                        filtered_data, 
                        y=sign_label, 
                        x="Fecha", 
                        width=300, 
                        height=200,
                        color=colors[i]
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)