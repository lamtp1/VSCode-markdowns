        try:
            existing_df = pd.read_csv("thong_tin_instance.csv")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass