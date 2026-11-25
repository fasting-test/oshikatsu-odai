// Google Apps Script のウェブアプリURLを設定する(セットアップは README.md を参照)。
// 管理者の合言葉は、ここではなく、Apps Script側のスクリプトプロパティ ADMIN_PIN に保存する。
//
// 手元での確認(node scripts/serve.cjs)のときは、自動的に疑似サーバー "/gas" につながる。
//
// デモ環境: URLの末尾に ?demo=1 を付けると、デモ用のスプレッドシートにつながる(本番のデータには触れない)。
// デモでは、画面上の「今日」を demoToday として動かす(デモ用のApps Scriptにも TEST_TODAY を同じ日付で入れておく)。
;(function () {
  const isLocal = ["localhost", "127.0.0.1"].includes(location.hostname)
  const DEMO_ON = new URLSearchParams(location.search).get("demo") === "1"
  // 新しいスプレッドシートの Apps Script を公開したら、そのURLを入れる(推し活サイトとは別)
  const PRODUCTION_URL = ""
  const DEMO_URL = ""
  // デモ用の Apps Script を作るまでは、?demo=1 を付けても本番につながる(デモの表示にはしない)
  const isDemo = DEMO_ON && !!DEMO_URL
  window.APP_CONFIG = {
    demo: isDemo,
    demoToday: "2026-12-10",
    webAppUrl: isLocal ? "/gas" : isDemo ? DEMO_URL : PRODUCTION_URL,
  }
})()
