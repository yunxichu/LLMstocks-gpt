"""Stage 1+2 batch for /picks. Disposable scratch script."""
import json
import os
import sys
sys.path.insert(0, '.')
from data.web import a_share, calendar, benchmark

CANDIDATES = [
    ('600519.SH', '贵州茅台', 'watchlist'),
    ('002230.SZ', '科大讯飞', 'watchlist'),
    ('688256.SH', '寒武纪',   'ai-compute'),
    ('688041.SH', '海光信息', 'ai-compute'),
    ('601138.SH', '工业富联', 'ai-compute'),
    ('000977.SZ', '浪潮信息', 'ai-compute'),
    ('603019.SH', '中科曙光', 'ai-compute'),
    ('002463.SZ', '沪电股份', 'ai-compute'),
    ('300308.SZ', '中际旭创', 'optical-cpo'),
    ('300502.SZ', '新易盛',   'optical-cpo'),
    ('300394.SZ', '天孚通信', 'optical-cpo'),
    ('300620.SZ', '光库科技', 'optical-cpo'),
    ('688313.SH', '仕佳光子', 'optical-cpo'),
    ('002371.SZ', '北方华创', 'semi-equipment'),
    ('688012.SH', '中微公司', 'semi-equipment'),
    ('688072.SH', '拓荆科技', 'semi-equipment'),
    ('300604.SZ', '长川科技', 'semi-equipment'),
    ('688126.SH', '沪硅产业', 'semi-equipment'),
    ('688200.SH', '华峰测控', 'semi-equipment'),
    ('688017.SH', '绿的谐波', 'robotics'),
    ('601689.SH', '拓普集团', 'robotics'),
    ('603728.SH', '鸣志电器', 'robotics'),
    ('300660.SZ', '江苏雷利', 'robotics'),
    ('603667.SH', '五洲新春', 'robotics'),
    ('300274.SZ', '阳光电源', 'energy-storage'),
    ('300750.SZ', '宁德时代', 'energy-storage'),
    ('002028.SZ', '思源电气', 'energy-storage'),
    ('688676.SH', '金盘科技', 'energy-storage'),
    ('600522.SH', '中天科技', 'energy-storage'),
    ('300073.SZ', '当升科技', 'solid-state-battery'),
    ('688005.SH', '容百科技', 'solid-state-battery'),
    ('688778.SH', '厦钨新能', 'solid-state-battery'),
    ('300409.SZ', '道氏技术', 'solid-state-battery'),
    ('000099.SZ', '中信海直', 'low-altitude'),
    ('002085.SZ', '万丰奥威', 'low-altitude'),
    ('300699.SZ', '光威复材', 'low-altitude'),
    ('688631.SH', '莱斯信息', 'low-altitude'),
    ('600536.SH', '中国软件', 'domestic-software'),
    ('688111.SH', '金山办公', 'domestic-software'),
    ('600588.SH', '用友网络', 'domestic-software'),
    ('002405.SZ', '四维图新', 'domestic-software'),
    ('600760.SH', '中航沈飞', 'military-tech'),
    ('688375.SH', '国博电子', 'military-tech'),
    ('000733.SZ', '振华科技', 'military-tech'),
    ('600118.SH', '中国卫星', 'military-tech'),
    ('688122.SH', '西部超导', 'military-tech'),
    ('603259.SH', '药明康德', 'biotech-ai'),
    ('002821.SZ', '凯莱英',   'biotech-ai'),
    ('300676.SZ', '华大基因', 'biotech-ai'),
    ('300558.SZ', '贝达药业', 'biotech-ai'),
]


def main():
    print(f"=== Stage 1: candidate pool = {len(CANDIDATES)} tickers ===")
    entry_date = calendar.today_or_previous_trading_day()
    bm_close = benchmark.benchmark_close_on('000300.SH', entry_date)
    print(f"entry_date: {entry_date}")
    print(f"benchmark 000300.SH entry_close: {bm_close:.4f}")
    print()
    print("=== Stage 2: batch yfinance scoring ===")

    results = []
    for ticker, name, source in CANDIDATES:
        try:
            info = a_share.stock_info(ticker)
            sn = info.get('shortName') or info.get('longName') or ''
            is_st = 'ST' in sn.upper()
            mc = info.get('marketCap')
            pe = info.get('trailingPE')
            pb = info.get('priceToBook')
            roe = info.get('returnOnEquity')
            margin = info.get('profitMargins')
            sector = info.get('sector')

            hist = a_share.stock_history(ticker, period='6mo')
            close_now = float(hist['Close'].iloc[-1]) if not hist.empty else None
            ret_60d = ret_6mo = None
            if not hist.empty and len(hist) >= 60:
                ret_60d = close_now / float(hist['Close'].iloc[-60]) - 1
            if not hist.empty:
                ret_6mo = close_now / float(hist['Close'].iloc[0]) - 1

            ai = a_share.stock_financials(ticker)
            acf = a_share.stock_cashflow(ticker)
            abs_ = a_share.stock_balance_sheet(ticker)

            rev_cagr_3y = ni_cagr_3y = rev_yoy = ocf_ni_avg = gw_eq = None

            if not ai.empty:
                years = sorted([c for c in ai.columns])
                if len(years) >= 4 and 'Total Revenue' in ai.index:
                    r_old = ai.loc['Total Revenue', years[-4]]
                    r_new = ai.loc['Total Revenue', years[-1]]
                    r_prev = ai.loc['Total Revenue', years[-2]]
                    if r_old and r_old > 0:
                        rev_cagr_3y = (r_new / r_old) ** (1/3) - 1
                    if r_prev and r_prev > 0:
                        rev_yoy = r_new / r_prev - 1
                if len(years) >= 4 and 'Net Income' in ai.index:
                    n_old = ai.loc['Net Income', years[-4]]
                    n_new = ai.loc['Net Income', years[-1]]
                    if n_old and n_old > 0:
                        ni_cagr_3y = (n_new / n_old) ** (1/3) - 1

                if not acf.empty and 'Operating Cash Flow' in acf.index and 'Net Income' in ai.index:
                    ratios = []
                    for y in years:
                        if y in acf.columns:
                            ocf = acf.loc['Operating Cash Flow', y]
                            ni = ai.loc['Net Income', y]
                            if ni and ni > 0 and ocf is not None and not (isinstance(ocf, float) and ocf != ocf):
                                ratios.append(ocf / ni)
                    if ratios:
                        ocf_ni_avg = sum(ratios) / len(ratios)

            if not abs_.empty:
                latest_y = abs_.columns[0]
                if 'Stockholders Equity' in abs_.index:
                    e = abs_.loc['Stockholders Equity', latest_y]
                    g = abs_.loc['Goodwill', latest_y] if 'Goodwill' in abs_.index else 0
                    if isinstance(g, float) and g != g:
                        g = 0
                    if e and e > 0:
                        gw_eq = (g or 0) / e

            score = 50
            flags = []
            if is_st:
                score -= 30; flags.append('ST')
            if rev_cagr_3y is not None and rev_cagr_3y > 0.15:
                score += 15
            if ni_cagr_3y is not None and ni_cagr_3y > 0.15:
                score += 15
            if rev_yoy is not None and rev_yoy < -0.10:
                score -= 10; flags.append('REV_DECL')
            if roe is not None and roe > 0.20:
                score += 10
            if margin is not None and margin > 0.25:
                score += 5
            if ocf_ni_avg is not None and ocf_ni_avg < 0.5:
                score -= 20; flags.append('OCF_LOW')
            elif ocf_ni_avg is not None and ocf_ni_avg < 0.7:
                score -= 10; flags.append('OCF_MED')
            if gw_eq is not None and gw_eq > 0.5:
                score -= 20; flags.append('GW_HIGH')
            elif gw_eq is not None and gw_eq > 0.3:
                score -= 10; flags.append('GW_MED')
            if ret_60d is not None and ret_60d > 0.50:
                score -= 15; flags.append('HOT60')
            elif ret_60d is not None and ret_60d > 0.30:
                score -= 5; flags.append('UP60')
            if pe is not None and pe > 80:
                score -= 10; flags.append('PE_HI')
            elif pe is not None and pe < 0:
                score -= 10; flags.append('NEG_PE')

            row = {
                'ticker': ticker, 'name': name, 'name_yf': sn, 'source': source,
                'is_st': is_st, 'sector': sector,
                'market_cap_b': round(mc/1e9, 2) if mc else None,
                'pe': round(pe, 1) if pe is not None else None,
                'pb': round(pb, 2) if pb is not None else None,
                'roe_pct': round(roe*100, 1) if roe is not None else None,
                'margin_pct': round(margin*100, 1) if margin is not None else None,
                'ret_60d_pct': round(ret_60d*100, 1) if ret_60d is not None else None,
                'ret_6mo_pct': round(ret_6mo*100, 1) if ret_6mo is not None else None,
                'rev_cagr_3y_pct': round(rev_cagr_3y*100, 1) if rev_cagr_3y is not None else None,
                'rev_yoy_pct': round(rev_yoy*100, 1) if rev_yoy is not None else None,
                'ni_cagr_3y_pct': round(ni_cagr_3y*100, 1) if ni_cagr_3y is not None else None,
                'ocf_ni_avg_pct': round(ocf_ni_avg*100, 1) if ocf_ni_avg is not None else None,
                'gw_eq_pct': round(gw_eq*100, 1) if gw_eq is not None else None,
                'initial_score': score,
                'prelim_flags': flags,
                'entry_close': round(close_now, 2) if close_now else None,
            }
            results.append(row)
            print(f"  {ticker} {name[:8]:8s} | s={score:3d} | {','.join(flags) if flags else '-':25s} | pe={row['pe']} roe={row['roe_pct']}% rev3y={row['rev_cagr_3y_pct']}% ocf={row['ocf_ni_avg_pct']}% r60={row['ret_60d_pct']}%")
        except Exception as e:
            print(f"  {ticker} {name[:8]:8s} | ERROR: {str(e)[:80]}")
            results.append({'ticker': ticker, 'name': name, 'source': source, 'error': str(e)})

    os.makedirs('predictions/picks/2026-06-08', exist_ok=True)
    out_path = 'predictions/picks/2026-06-08/_scratch_stage2.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'entry_date': str(entry_date), 'benchmark_close': bm_close, 'results': results}, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 100)
    print(f"saved scratch -> {out_path}")
    print()
    valid = [r for r in results if 'error' not in r]
    valid.sort(key=lambda x: x['initial_score'], reverse=True)

    print("TOP 15 (BUY candidates by initial_score):")
    hdr = f"{'rank':4} {'ticker':10} {'name':10} {'score':5} {'sector':25} {'pe':>6} {'roe%':>6} {'rev3y%':>7} {'rev_y%':>7} {'ocf%':>6} {'r60d%':>6} {'gw%':>5} flags"
    print(hdr)
    for i, r in enumerate(valid[:15]):
        print(f"{i+1:4} {r['ticker']:10} {r['name'][:10]:10} {r['initial_score']:5} {(r.get('sector') or '?')[:25]:25} {str(r.get('pe', '-')):>6} {str(r.get('roe_pct', '-')):>6} {str(r.get('rev_cagr_3y_pct', '-')):>7} {str(r.get('rev_yoy_pct', '-')):>7} {str(r.get('ocf_ni_avg_pct', '-')):>6} {str(r.get('ret_60d_pct', '-')):>6} {str(r.get('gw_eq_pct', '-')):>5} {','.join(r.get('prelim_flags', []))}")
    print()
    print("BOTTOM 15 (AVOID candidates by initial_score, ascending):")
    print(hdr)
    for i, r in enumerate(valid[-15:]):
        print(f"{len(valid)-14+i:4} {r['ticker']:10} {r['name'][:10]:10} {r['initial_score']:5} {(r.get('sector') or '?')[:25]:25} {str(r.get('pe', '-')):>6} {str(r.get('roe_pct', '-')):>6} {str(r.get('rev_cagr_3y_pct', '-')):>7} {str(r.get('rev_yoy_pct', '-')):>7} {str(r.get('ocf_ni_avg_pct', '-')):>6} {str(r.get('ret_60d_pct', '-')):>6} {str(r.get('gw_eq_pct', '-')):>5} {','.join(r.get('prelim_flags', []))}")


if __name__ == '__main__':
    main()
