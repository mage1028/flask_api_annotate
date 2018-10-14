import dva, { connect } from 'dva';
import { Router, Route } from 'dva/router';
import React from 'react';
import styles from './index.less';

const app = dva();

app.model({
  namespace: 'count',

  state: {
    record: 0,
    current: 0,
  },

  reducers: {

    add(state) {
      const newCurrent = state.current + 1;
      return {

        record: newCurrent > state.record ? newCurrent : state.record,
        current: newCurrent,
      };
    },

  },

});

const CountApp = ({count, dispatch}) => {
  return (
    <div className={styles.normal}>
      <div className={styles.record}>Highest Record: {count.record}</div>

      <div className={styles.current}>{count.current}</div>

      <div className={styles.button}>
        <button onClick={() => { dispatch({type: 'count/add'}); }}>+</button>
      </div>
    </div>
  );
};

function mapStateToProps(state) //输入 state
{
  return { count: state.count };// 输入从count来
}
const HomePage = connect(mapStateToProps)(CountApp); //映射到CountApp 接收到了app(count)的数据， 变量为count

app.router(({history}) =>
  <Router history={history}>
    <Route path="/" component={HomePage} />
  </Router>
);

app.start('#root');


// ---------
// Helpers

function delay(timeout){
  return new Promise(resolve => {
    setTimeout(resolve, timeout);
  });
}
