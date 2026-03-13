import Hero from "./components/Hero";
import Header from "./components/Header";
import Metric from "./components/Metric";
import Footer from "./components/Footer";

function App() {
  return (
    <main className="text-white font-neue-machina box-border">
      <section className="border-0 bg-background relative flex flex-col gap-10 overflow-hidden p-10 z-0">
        <Header />
        <Hero />
      </section>
      <Metric />
      {/* Footer Section */}
      <Footer />
    </main>
  );
}

export default App;
