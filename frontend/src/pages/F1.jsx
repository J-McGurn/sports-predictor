import { useEffect, useState } from "react";
import {
  DndContext,
  closestCenter,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
} from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import "./Sport.css";

import {
  getActiveSeasons,
  getF1Drivers,
  getF1Constructors,
  getF1DriverPrediction,
  getF1ConstructorPrediction,
  saveF1DriverPrediction,
  saveF1ConstructorPrediction,
} from "../services/api";


function SortableItem({ item, position }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: item.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="prediction-row"
    >
      <div className="prediction-position">
        {position}
      </div>

      <div className="prediction-team">
        <strong>{item.name}</strong>

        {item.constructor && (
          <span className="prediction-secondary">
            {item.constructor.name}
          </span>
        )}
      </div>

      <button
        type="button"
        className="drag-handle"
        {...attributes}
        {...listeners}
        aria-label={`Move ${item.name}`}
      >
        ☰
      </button>
    </div>
  );
}


function PredictionList({
  items,
  setItems,
  title,
  description,
  onSave,
  saving,
}) {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5,
      },
    })
  );

  function handleDragEnd(event) {
    const { active, over } = event;

    if (!over || active.id === over.id) {
      return;
    }

    setItems((currentItems) => {
      const oldIndex = currentItems.findIndex(
        (item) => item.id === active.id
      );

      const newIndex = currentItems.findIndex(
        (item) => item.id === over.id
      );

      return arrayMove(
        currentItems,
        oldIndex,
        newIndex
      );
    });
  }

  return (
    <section className="prediction-section">

      <div className="prediction-instructions">
        <h2>{title}</h2>
        <p>{description}</p>
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={items.map((item) => item.id)}
          strategy={verticalListSortingStrategy}
        >
          <div className="prediction-table">

            <div className="prediction-table-header">
              <span>Position</span>
              <span>Driver / Constructor</span>
              <span></span>
            </div>

            {items.map((item, index) => (
              <SortableItem
                key={item.id}
                item={item}
                position={index + 1}
              />
            ))}

          </div>
        </SortableContext>
      </DndContext>

      <div className="prediction-actions">
        <button
          type="button"
          onClick={onSave}
          disabled={saving}
        >
          {saving ? "Saving..." : `Save ${title}`}
        </button>
      </div>

    </section>
  );
}


function F1() {
  const [season, setSeason] = useState(null);

  const [drivers, setDrivers] = useState([]);
  const [constructors, setConstructors] = useState([]);

  const [loading, setLoading] = useState(true);

  const [driverSaving, setDriverSaving] = useState(false);
  const [constructorSaving, setConstructorSaving] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");


  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        setError("");

        const seasonData = await getActiveSeasons();

        const f1Season = seasonData.seasons.find(
          (season) => season.sport === "F1"
        );

        if (!f1Season) {
          throw new Error(
            "No active Formula 1 season found."
          );
        }

        setSeason(f1Season);

        const [
          driverData,
          constructorData,
        ] = await Promise.all([
          getF1Drivers(f1Season.id),
          getF1Constructors(f1Season.id),
        ]);

        let loadedDrivers = driverData.drivers;
        let loadedConstructors =
          constructorData.constructors;

        try {
          const prediction =
            await getF1DriverPrediction(
              f1Season.id
            );

          if (
            prediction.predictions &&
            prediction.predictions.length === 22
          ) {
            loadedDrivers =
              prediction.predictions.map(
                (item) => item.driver
              );
          }
        } catch {
          // No saved prediction yet.
        }

        try {
          const prediction =
            await getF1ConstructorPrediction(
              f1Season.id
            );

          if (
            prediction.predictions &&
            prediction.predictions.length === 11
          ) {
            loadedConstructors =
              prediction.predictions.map(
                (item) => item.constructor
              );
          }
        } catch {
          // No saved prediction yet.
        }

        setDrivers(loadedDrivers);
        setConstructors(loadedConstructors);

      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);


  async function handleSaveDrivers() {
    try {
      setDriverSaving(true);
      setError("");
      setSuccess("");

      const predictions = drivers.map(
        (driver, index) => ({
          driver_id: driver.id,
          position: index + 1,
        })
      );

      await saveF1DriverPrediction(
        season.id,
        predictions
      );

      setSuccess(
        "Drivers' Championship prediction saved."
      );
    } catch (error) {
      setError(error.message);
    } finally {
      setDriverSaving(false);
    }
  }


  async function handleSaveConstructors() {
    try {
      setConstructorSaving(true);
      setError("");
      setSuccess("");

      const predictions = constructors.map(
        (constructor, index) => ({
          constructor_id: constructor.id,
          position: index + 1,
        })
      );

      await saveF1ConstructorPrediction(
        season.id,
        predictions
      );

      setSuccess(
        "Constructors' Championship prediction saved."
      );
    } catch (error) {
      setError(error.message);
    } finally {
      setConstructorSaving(false);
    }
  }


  if (loading) {
    return (
      <main className="sport-page">
        <div className="sport-page-container">
          <p>Loading Formula 1...</p>
        </div>
      </main>
    );
  }


  if (error && !season) {
    return (
      <main className="sport-page">
        <div className="sport-page-container">
          <div className="auth-error">
            {error}
          </div>
        </div>
      </main>
    );
  }


  return (
    <main className="sport-page">
      <div className="sport-page-container">

        <header className="sport-page-header">
          <h1>Formula 1</h1>

          <p>
            Predict the championships for{" "}
            <strong>{season.name}</strong>.
          </p>
        </header>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        {success && (
          <div className="prediction-success">
            {success}
          </div>
        )}

        <PredictionList
          items={drivers}
          setItems={setDrivers}
          title="Drivers' Championship"
          description="Predict the final Drivers' Championship standings."
          onSave={handleSaveDrivers}
          saving={driverSaving}
        />

        <PredictionList
          items={constructors}
          setItems={setConstructors}
          title="Constructors' Championship"
          description="Predict the final Constructors' Championship standings."
          onSave={handleSaveConstructors}
          saving={constructorSaving}
        />

      </div>
    </main>
  );
}

export default F1;