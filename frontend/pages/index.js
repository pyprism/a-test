import Head from 'next/head';
import styles from '../styles/Home.module.css';
import React from "react";

export default function Home() {
    const [keywordState, setKeywordState] = React.useState("");
    const [data, setData] = React.useState("");
    const [isLoading, setLoading] = React.useState(true);

    const getEmployee = async (cto) => {
        const employee = await fetch(`http://0.0.0.0:8000/v1/api/employee/get_all_employee/?cto_id=${cto}`);  // just for demo, but not a best practice to use static url here
        if (employee.status === 200) {
            const response = await employee.json();
            console.log(response);
            setData(response);
            setLoading(false);
        } else {
            setData("");
        }
    };

    const handleChange = (e) => {
        const value = e.target.value;
        setKeywordState(value);
        if(value.length > 0) {
            setLoading(true);
            getEmployee(value)
        }

    }

    const gridEmployee = (data) => {
        if(data.length > 0) {
            return data.map((item, index) => {
                return (
                    <div className={styles.card} key={index}>
                        <h2>Employee name  {item['name']}</h2>
                        <p>Employee type: {item['employee_type']} </p>
                    </div>
                )
            })
        }
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>Get Employee By CTO ID</title>
            </Head>

            <main className={styles.main}>
                <h1 className={styles.title}>
                    Get Employee By CTO ID
                </h1>

                <p className={styles.description}>
                    <input className="input has-shadow is-medium is-rounded"
                           type="text"
                           placeholder="type cto id ex: 1"
                           name="keyword"
                           onChange={handleChange}
                           value={keywordState}
                    />
                </p>

            <div className={styles.grid}>
                {isLoading ? null: gridEmployee(data)}
            </div>
            </main>
        </div>
    )
}
